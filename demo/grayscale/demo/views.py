from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

import xml.etree.ElementTree as ET
import json
import logging
import sign_url
import subprocess
import re
import os
import uuid
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/src/pipeline')
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/external/mu/src/lambdaize/')

import pipeline
import pdb

# Get an instance of a logger
logger = logging.getLogger(__name__)
lambdas = "200"

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'static/index.html', context=None)

@csrf_exempt
def call_mu(request):
    if request.method == 'POST' and request.is_ajax():
        url = request.POST['url']
	logfile = request.POST['log']
	print ("URL=%s Logfile=%s") % (url, logfile)

    mpd_url, err = invoke_pipeline(url)
    response_data = {}
    response_data['mpd_url'] = mpd_url

    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

@csrf_exempt
def call_mu_stub(request):
    response_data = {}
    response_data['input_signed_url'] = 'http://dash.edgesuite.net/envivio/EnvivioDash3/manifest.mpd'
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@csrf_exempt
def invoke_pipeline(url):
    if not url.startswith('s3://'):
        # # for youtube videos:
        # # download video, upload to s3
        # # invoke pipeline
        # # get first mpd, modify
        # prefix = str(uuid.uuid4().get_hex().upper()[0:8])
        # if os.system("/srv/www/excamera/demo/grayscale/demo/youtube-dl -o 'temp/"+prefix+".%(ext)s' " + url) == 0:
        #     filename = os.popen('ls '+'temp/'+prefix+'*').read().strip()
        #     logger.info('downloaded video: ' + filename)
        #     if os.system("aws s3 cp " + filename + ' s3://lixiang-lambda-test/input/') == 0:
        #         logger.info(filename + " uploaded to s3")
        # url = 's3://lixiang-lambda-test/input/' + '/'.join(filename.split('/')[1:])

        # for youtube videos:
        # get video url using youtube-dl
        # invoke pipeline with the url
        # get first mpd, modify
        url_list = subprocess.check_output('youtube-dl --get-url '+url, stderr=subprocess.STDOUT, shell=True).split('\n')
        for u in url_list:
            if u.startswith('http'):
                video_url = u
                break
    print 'invoking pipeline with url: ' + video_url
    return pipeline.invoke(video_url, [('grayscale',[])])
    

@csrf_exempt
def invoke_mu(url, logfile):
    response_data = {}
    regex = "^https?://s3.amazonaws.com/(\S+)/(\S+)$"
    m = re.match(regex, url)
    if m:
        region = m.group(1)
        bucket = m.group(2)
        key    = m.group(3)
        print "region=%s bucket=%s key=%s" % (region, bucket, key)
        signed_url = sign_url.get_signed_url(3000, bucket, key)
        print "signed_url=%s" % signed_url
        response_data['input_signed_url'] = signed_url

        cmds = ["/home/kvasukib/lambda/pipeline/external/mu/src/lambdaize/run_pipeline.sh", 
                bucket, 
                key
		]
        try:
            print "Running the job in mu : "
            output = subprocess.check_output(cmds, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as exc:
            print ("error code", exc.returncode, exc.output)
            print "Job over from mu. Rendering the video..."
            return response_data
