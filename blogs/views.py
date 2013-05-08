# -*- coding: utf-8 -*-
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
	autosave_post.text = request.POST.get('text')
	autosave_post.save()

	return HttpResponse('updated successfully')
	
def sitemap(request):
	template_vars = {}
	template_vars['posts'] = Post.objects.values('id', 'createdAt').order_by('-id').all()

	return render_to_response (
		'blog/sitemap.xml', 
		template_vars, 
		mimetype = 'application/xml'
	)

def rss(request):
	template_vars = {}
	template_vars['posts'] = Post.objects.filter(visible=True).order_by('-id')[:7]

	return render_to_response (
		'blog/rss.xml', 
		template_vars, 
		context_instance = RequestContext(request), 
		mimetype = 'application/xml'
	)
	
def id(request, id, blog_post=None):
	template_vars = {}

	if not blog_post: 
		blog_post = get_object_or_404(Post, pk=id)

	template_vars['posts'] = [blog_post]
	template_vars['og_post'] = blog_post
	template_vars['title'] = blog_post.title

	if blog_post.slug and id == None:
		return HttpResponsePermanentRedirect(reverse('blogs.views.slug', args=[blog_post.slug]))

	return render_to_response (
		'blog/posts.html', 
		pimp_my_template(template_vars), 
		context_instance = RequestContext(request)
	)
	

def slug(request, slug):
	return id (
		request = request,
		blog_post = get_object_or_404(Post, slug=slug), 
		id = None
	)

def tag(request, tag, page=1):
	template_vars = {}
	pagination = Paginator(Post.objects.filter(tags__slug=tag, visible=True).order_by('-id'), 5)
		
	try:
		template_vars['current_page'] = pagination.page(page)
	except EmptyPage: 
		raise Http404

	template_vars['posts'] = template_vars['current_page'].object_list
	template_vars['pagination_url'] = '/blog/tag/{0}/page/'.format(tag)
	template_vars['pagination'] = pagination
	template_vars['page'] = page
		
	return render_to_response (
		'blog/posts.html', 
		pimp_my_template(template_vars), 
		context_instance=RequestContext(request)
	)

def index(request, page=1):
	template_vars = {}
	pagination = Paginator(Post.objects.filter(visible=True).order_by('-id'), 5)
		
	try:
		template_vars['current_page'] = pagination.page(page)
	except EmptyPage: 
		raise Http404

	template_vars['posts'] = template_vars['current_page'].object_list
	template_vars['pagination_url'] = '/blog/page/'
	template_vars['pagination'] = pagination
	template_vars['page'] = page
	
	return render_to_response (
		'blog/posts.html', 
		pimp_my_template(template_vars), 
		context_instance=RequestContext(request)
	)	

def pimp_my_template(template):
	template['randomMohos'] = Moho.objects.filter(visible=True).values('id', 'year', 'slug', 'title', 'imageURL').order_by('?')[:7]

	return template