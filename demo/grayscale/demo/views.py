from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def index(request):
    return render(request, 'static/index.html', context=None)

def call_mu(request):
    if request.method == 'POST':
	url = request.POST.get('url')
	bucket = request.POST.get('bucket')
	print ("URL=%s,Bucket=%s") % (url, bucket)
	response_data = {}
	output_mpd = invoke_mu(ur, bucket)
	response_data['mpd'] = output_mpd
	return HttpResponse(
	    json.dumps(response_data),
	    content_type="application/json"
	)

def invoke_mu(url, bucket):
	return "http://dash.edgesuite.net/envivio/EnvivioDash3/manifest.mpd"
