from instagram.client import InstagramAPI

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response

def index(request):
	return HttpResponsePermanentRedirect(settings.INSTAGRAM_URL)

def rss(request):
	api = InstagramAPI(access_token=settings.INSTAGRAM_TOKEN)

	media, next = api.user_recent_media(user_id=settings.INSTAGRAM_UID, count=20)

	return render_to_response (
		'hipstagram/rss.xml', 
		{ 'media': media }, 
		mimetype='application/xml'
	) 