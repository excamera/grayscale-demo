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
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../external/pipeline/src/pipeline')

from service import pipeline_pb2_grpc, pipeline_pb2
from config import settings
import time
import grpc
import pdb
import traceback
import ast


logger = logging.getLogger(__name__)


@csrf_exempt
def index(request):
    return render(request, 'static/index.html', context=None)


@csrf_exempt
def jobs(request):
    if request.method == 'POST' and request.is_ajax():
        try:

            video_link = request.POST['video_link']
            pipespec = request.POST['pipespec']
	    try:
	    	googleFaceInputRead = str(request.POST['googleFaceInput'])	
	    except Exception as e:
            	print "google Face Excpetion is " + str(e)
		return

	    # update rek pipespec with input
	    d = ast.literal_eval(pipespec)
	    if len(d['nodes']) >= 4 and d['nodes'][3]['name'] == 'rek':
	       	d['nodes'][3]['config']['person'] = googleFaceInputRead
	    pipespec = str(d).replace("'", '"')

            mpd_url = invoke_pipeline(video_link, pipespec)
            response_data = {}
            response_data['mpd_url'] = mpd_url
            return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json")
        except Exception as e:
	    print "Excpetion is", e, traceback.format_exc()
            return HttpResponse(content=str(e), status=500)
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def invoke_pipeline(url, pipespec):
    inputs = []
    input = pipeline_pb2.Input()
    input.type = 'video_link'
    input.value = str(url)
    inputs.append(input)

    d = ast.literal_eval(pipespec)

    if len(d['nodes']) >= 4 and d['nodes'][3]['name'] == 'rek':
        input = pipeline_pb2.Input()
        input.type = 'person'
        input.value = d['nodes'][3]['config']['person'] 
        inputs.append(input)

    channel = grpc.insecure_channel('%s:%d' % (settings['daemon_addr'], settings['daemon_port']))
    stub = pipeline_pb2_grpc.PipelineStub(channel)
    response = stub.Submit(pipeline_pb2.SubmitRequest(pipeline_spec=pipespec, inputs=inputs))

    if response.success:
        print time.time(), 'FORREST: finish pipeline, returning to browser'
        return response.mpd_url
    else:
        raise Exception(response.error_msg)
