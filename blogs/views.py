# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.conf import settings

from django.http import Http404

from blogs.models import Post
from mohos.models import Moho

from json import dumps

# GODMODE hacks
@user_passes_test(lambda u: u.is_superuser)
def upload_file(request):
	upload_destination = settings.MEDIA_ROOT + "blog_uploads/"

	if len(request.FILES) == 0:
		return HttpResponseNotFound('nothing to upload')

	try:
		file_for_upload = request.FILES['file']
	except:
		return HttpResponseNotFound('nothing to upload')

	upload_destination = upload_destination + str(file_for_upload.size) +'_' + file_for_upload.name
	destination_file = open(upload_destination, 'w')

	if file_for_upload.multiple_chunks:
		for chunk in file_for_upload.chunks():
			destination_file.write(chunk)
	else:
		destination_file.write(file_for_upload.read())

	destination_file.close()

	return HttpResponse(dumps({'filelink':upload_destination.replace(settings.MEDIA_ROOT, '/media/')}))

@user_passes_test(lambda u: u.is_superuser)
def autosave_post(request):
	try:
		autosave_post = Post.objects.get(id=request.GET['id'])
		autosave_post.text = request.POST['text']
		autosave_post.save()
	except:
		HttpResponse('updated unsuccessfully')
	return HttpResponse('updated successfully')

def sitemap(request):
	template_vars = {}
	template_vars['posts'] = Post.objects.values('id','createdAt').order_by('-id').all()
	return render_to_response('blog/sitemap.xml', template_vars, mimetype='application/xml')

def rss(request):
	template_vars = {}
	template_vars['posts'] = Post.objects.filter(visible=True).order_by('-id')[:7]
	return render_to_response('blog/rss.xml', template_vars, context_instance=RequestContext(request), mimetype='application/xml')
	
def id(request, id):
	template_vars = {}
	try:
		template_vars['posts'] = [Post.objects.get(id=id)]
		template_vars['og_post'] = template_vars['posts'][0]
		template_vars['title'] = template_vars['posts'][0].title + ' @ mindcollapse.com'
		return render_to_response('blog/posts.html', pumpTemplate(template_vars), context_instance=RequestContext(request))
	except:
		raise Http404

def tag(request, tag, page=1):
	template_vars = {}
		
	pagination = Paginator(Post.objects.filter(tags__slug=tag, visible=True).order_by('-id'), 5)
		
	try:
		template_vars['posts'] = pagination.page(page).object_list
		template_vars['current_page'] = pagination.page(page)
		template_vars['title'] = tag.title() + ' @ mindcollapse.com'
		template_vars['pagination_url'] = '/blog/tag/' + tag + '/page/'
		template_vars['pagination'] = pagination
		template_vars['page'] = page
		
	except:
		raise Http404

	return render_to_response('blog/posts.html', pumpTemplate(template_vars), context_instance=RequestContext(request))

def index(request, page=1):
	template_vars = {}
		
	pagination = Paginator(Post.objects.filter(visible=True).order_by('-id'), 5)
		
	try:
		template_vars['posts'] = pagination.page(page).object_list
		template_vars['current_page'] = pagination.page(page)
		template_vars['pagination_url'] = '/blog/page/'
		template_vars['pagination'] = pagination
		template_vars['page'] = page
		
	except:
		raise Http404
	return render_to_response('blog/posts.html', pumpTemplate(template_vars), context_instance=RequestContext(request))	
	

def pumpTemplate(template):
	template['randomMohos'] = Moho.objects.filter(visible=True).values('id', 'year', 'slug', 'title', 'imageURL').order_by('?')[:7]
	return template
	
