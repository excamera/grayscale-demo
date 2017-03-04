from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

import json
import logging
import sign_url
import subprocess
import re
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)
lambdas = "200"

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'static/index.html', context=None)

@csrf_exempt
def call_mu(request):
    if request.method == 'POST':
        print (request.POST)
        url = request.POST.get("url")
        print ("URL=%s") % url
        response_data = invoke_mu(url)
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

def invoke_pipeline(url):
    pass

def invoke_mu(url):
    response_data = {}
    url = "https://s3-us-west-2.amazonaws.com/excamera-ffmpeg-input/input.mp4"
    regex = "^https://s3-(\S+).amazonaws.com/(\S+)/(\S+)$"
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
                key]
        try:
            print "Running the job in mu : "
            output = subprocess.check_output(cmds, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as exc:
            print ("error code", exc.returncode, exc.output)
            print "Job over from mu. Rendering the video..."
            return response_data
