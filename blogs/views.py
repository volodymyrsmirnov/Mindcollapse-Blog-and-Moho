# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator

from blogs.models import Post
from mohos.models import Moho

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
        return HttpResponseNotFound()

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
		return HttpResponseNotFound()

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
		return HttpResponseNotFound()
	return render_to_response('blog/posts.html', pumpTemplate(template_vars), context_instance=RequestContext(request))	
	

def pumpTemplate(template):
	template['randomMohos'] = Moho.objects.filter(visible=True).values('id', 'year', 'title', 'imageURL').order_by('?')[:7]
	return template
	
