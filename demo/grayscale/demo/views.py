from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'static/index.html', context=None)

@csrf_exempt
def call_mu(request):
    if request.method == 'POST':
	print (request)
	url = request.POST.get('url')
	bucket = request.POST.get('bucket')
	print ("URL=%s,Bucket=%s") % (url, bucket)
	response_data = {}
	output_mpd = invoke_mu(url, bucket)
	response_data['mpd'] = output_mpd
	return HttpResponse(
	    json.dumps(response_data),
	    content_type="application/json"
	)

def invoke_mu(url, bucket):
	script = "/home/kvasukib/lambda/pipeline/external/mu/src/lambdaize/run_pipeline.sh " + bucket
	mpd = "http://dash.edgesuite.net/envivio/EnvivioDash3/manifest.mpd"
	print (mpd)
	return mpd
