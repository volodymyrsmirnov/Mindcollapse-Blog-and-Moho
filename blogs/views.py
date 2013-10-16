# -*- coding: utf-8 -*-
import urllib2

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.conf import settings

from django.http import Http404

from blogs.models import Post
from mohos.models import Moho

from json import dumps

@user_passes_test(lambda u: u.is_superuser)
def upload_file(request):
	upload_destination = '{0}blog_uploads/'.format(settings.MEDIA_ROOT)

	if len(request.FILES) == 0:
		return HttpResponseNotFound('nothing to upload')

	try:
		file_for_upload = request.FILES['file']
	except:
		return HttpResponseNotFound('nothing to upload')

	upload_destination = '{0}{1}_{2}'.format(upload_destination, file_for_upload.size, file_for_upload.name)

	destination_file = open(upload_destination, 'w')

	if file_for_upload.multiple_chunks:
		for chunk in file_for_upload.chunks():
			destination_file.write(chunk)
	else:
		destination_file.write(file_for_upload.read())

	destination_file.close()

	return HttpResponse (
		dumps ({
			'filelink': upload_destination.replace(settings.MEDIA_ROOT, '/media/')
		})
	)

@user_passes_test(lambda u: u.is_superuser)
def autosave_post(request):

	if request.GET.get('id') == None:
		return HttpResponse('save the post first')

	autosave_post = get_object_or_404(Post, id=int(request.GET.get('id'))) 
	autosave_post.text = urllib2.unquote(request.POST.get('text').encode('ascii'))
	autosave_post.save()

	return HttpResponse('updated successfully')
	
def sitemap(request):
	template_vars = {}
	template_vars['posts'] = Post.objects.values('id', 'createdAt').order_by('-id').all()

	return render_to_response ("blog/sitemap.xml", template_vars, mimetype="application/xml")

def rss(request):
	template_vars = {}
	template_vars['posts'] = Post.objects.filter(visible=True).order_by('-id')[:7]

	return render_to_response ("blog/rss.xml", template_vars, mimetype="application/xml")

def archive(request):
	template_vars = {
		"title": "Архив записей",
		"archive": True,
	}

	template_vars["posts"] = Post.objects.values("id", "slug", "title", "createdAt").order_by("-id").all()

	return render_to_response ("blog/archive.html", template_vars)
	
def id(request, id, blog_post=None):
	template_vars = {}

	if not blog_post: 
		blog_post = get_object_or_404(Post, pk=id)

	template_vars["post"] = blog_post
	template_vars["title"] = blog_post.title

	if blog_post.slug and id != None:
		return HttpResponsePermanentRedirect(reverse("blogs.views.slug", args=[blog_post.slug]))

	return render_to_response ("blog/post.html", template_vars)
	
def slug(request, slug):
	return id(request=request, blog_post=get_object_or_404(Post, slug=slug), id=None)

def index(request, page=1):
	post = Post.objects.filter(visible=True).order_by("-id")[0]

	if post.slug:
		url = reverse("blogs.views.slug", args=[post.slug])
	else:
		url = reverse("blogs.views.id", args=[post.id])

	return HttpResponseRedirect(url)
	
