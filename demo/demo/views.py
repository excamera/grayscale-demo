from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
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
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/pipeline/src/pipeline')

from service import pipeline_pb2_grpc, pipeline_pb2
from config import settings
import time
import grpc
import pdb

logger = logging.getLogger(__name__)


@csrf_exempt
def index(request):
    return render(request, 'static/index.html', context=None)


@csrf_exempt
def jobs(request):
    # pdb.set_trace()
    if request.method == 'POST' and request.is_ajax():
        try:
            video_link = request.POST['video_link']
            pipespec = request.POST['pipespec']

            mpd_url = invoke_pipeline(video_link, pipespec)
            response_data = {}
            response_data['mpd_url'] = mpd_url
            pdb.set_trace()
            return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json")
        except Exception as e:
            return HttpResponse(content=str(e), status=500)
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def invoke_pipeline(url, pipespec):
    print time.time(), 'FORREST: invoking pipeline:', time.time()
    if not url.startswith('s3://'):
        # for youtube videos:
        # get video url using youtube-dl
        # invoke pipeline with the url
        # get first mpd, modify
        url_list = subprocess.check_output('youtube-dl --get-url '+url, stderr=subprocess.STDOUT, shell=True).split('\n')
        for u in url_list:
            if u.startswith('http'):
                video_url = u
                break
    print time.time(), 'FORREST: get actually video url'
    channel = grpc.insecure_channel('%s:%d' % (settings['daemon_addr'], settings['daemon_port']))
    stub = pipeline_pb2_grpc.PipelineStub(channel)
    response = stub.Submit(pipeline_pb2.PipelineRequest(pipeline_spec=pipespec, input_urls=[video_url], options=None))

    if response.success:
        print time.time(), 'FORREST: finish pipeline, returning to browser'
        return response.mpd_url
    else:
        raise Exception(response.error_msg)
