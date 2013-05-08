# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

from mohos.models import Moho

def index(request):
	template_vars = {
		'ajaxType': 'main'
	}

	template_vars = pimp_my_template(template_vars)
	template_vars['scrollCount'] = template_vars['mohosTotalCount']
	template_vars['reviews'] = Moho.objects.filter(visible=True).order_by('-id')[:7]

	return render_to_response (
		'moho/reviews.html', 
		template_vars, 
		context_instance=RequestContext(request)
	)
	
def genre(request,genre):
	template_vars = {}
	template_vars['scrollCount'] = Moho.objects.filter(visible=True, genres__slug=genre).count()
	
	if template_vars['scrollCount']	< 7: 
		template_vars = {
			'disableAJAX': 'true'
		}
	else: 
		template_vars['ajaxType'] = 'genre&genre={0}'.format(genre)
	
	template_vars['reviews'] = Moho.objects.filter(visible=True, genres__slug=genre).order_by('-id')[:7]

	if template_vars['reviews'].count() == 0: 
		raise Http404
	else: 
		template_vars['title'] = u'Фильмы жанра {0}'.format(genre.title())

		return render_to_response (
			'moho/reviews.html', 
			pimp_my_template(template_vars), 
			context_instance=RequestContext(request)
		)
		
def actor(request,actor):
	template_vars = {}
	template_vars['scrollCount'] = Moho.objects.filter(visible=True, actors__slug=actor).count()
	
	if template_vars['scrollCount']	< 7: 
		template_vars = {
			'disableAJAX': 'true'
		}
	else: 
		template_vars['ajaxType'] = 'actor&actor={0}'.format(actor)
	
	template_vars['reviews'] = Moho.objects.filter(visible=True, actors__slug=actor).order_by('-id')[:7]

	if template_vars['reviews'].count() == 0: 
		raise Http404
	else: 
		template_vars['title'] = u'Фильмы с участием {0}'.format(actor.title())

		return render_to_response (
			'moho/reviews.html', 
			pimp_my_template(template_vars), 
			context_instance=RequestContext(request)
		)
		
def director(request,director):
	template_vars = {}
	template_vars['scrollCount'] = Moho.objects.filter(visible=True, directors__slug=director).count()
	
	if template_vars['scrollCount']	< 7: 
		template_vars = {
			'disableAJAX':'true'
		}
	else: 
		template_vars['ajaxType'] = 'director&director={0}'.format(director)
	
	template_vars['reviews'] = Moho.objects.filter(visible=True, directors__slug=director).order_by('-id')[:7]

	if template_vars['reviews'].count() == 0: 
		raise Http404
	else: 
		template_vars['title'] = u'Фильмы, снятые {0}'.format(director.title())

		return render_to_response (
			'moho/reviews.html', 
			pimp_my_template(template_vars), 
			context_instance=RequestContext(request)
		)
	
def sitemap(request):
	template_vars = {}
	template_vars['reviews'] = Moho.objects.values('id', 'year', 'slug', 'createdAt').order_by('-id').filter(visible=True)

	return render_to_response (
		'moho/sitemap.xml', 
		template_vars, 
		mimetype='application/xml'
	)
	
def rss(request):
	template_vars = {}

	if request.REQUEST.get('type') == "like":
		template_vars['reviews'] = Moho.objects.filter(visible=True, like=True).order_by('-id')[:7]
	elif request.REQUEST.get('type') == "dislike":
		template_vars['reviews'] = Moho.objects.filter(visible=True, like=False).order_by('-id')[:7]
	else:
		template_vars['reviews'] = Moho.objects.filter(visible=True).order_by('-id')[:7]
		
	return render_to_response (
		'moho/rss.xml', 
		template_vars, 
		mimetype='application/xml'
	) 
		
def ajax(request):
	template_vars = {}
	
	startFrom = 7  * int(request.REQUEST.get('page'))
	endWith = startFrom + 7

	if request.REQUEST.get('type') == 'main': 
		template_vars['reviews'] = Moho.objects.filter(visible=True).order_by('-id')[startFrom:endWith]
	elif request.REQUEST.get('type') == 'like': 
		template_vars['reviews'] = Moho.objects.filter(visible=True, like=True).order_by('-id')[startFrom:endWith]
	elif request.REQUEST.get('type') == 'dislike': 
		template_vars['reviews'] = Moho.objects.filter(visible=True, like=False).order_by('-id')[startFrom:endWith]
	elif request.REQUEST.get('type') ==  'year':
		template_vars['reviews'] = Moho.objects.filter(visible=True, year=int(request.REQUEST.get('year'))).order_by('-id')[startFrom:endWith]
	elif request.REQUEST.get('type') ==  'genre':	
		template_vars['reviews'] = Moho.objects.filter(visible=True, genres__slug=request.REQUEST.get('genre')).order_by('-id')[startFrom:endWith]
	elif request.REQUEST.get('type') ==  'actor':	
		template_vars['reviews'] = Moho.objects.filter(visible=True, actors__slug=request.REQUEST.get('actor')).order_by('-id')[startFrom:endWith]
	else: 
		raise Http404
	
	if template_vars['reviews'].count() == 0: 
		raise Http404
	else: 
		return render_to_response (
			'moho/items.html', 
			template_vars, 
			context_instance=RequestContext(request)
		)

def attitude(request, attitude):
	template_vars = {}
	template_vars = pimp_my_template(template_vars)
	
	if attitude == 'like': 
		like = True
		template_vars['ajaxType'] = 'like'
		template_vars['title'] = u'Фильмы, которые мне понравились'
		template_vars['scrollCount'] = template_vars['mohosLikeCount']
	else:
		like = False
		template_vars['ajaxType'] = 'dislike'
		template_vars['title'] = u'Фильмы, которые мне не понравились'
		template_vars['scrollCount'] = template_vars['mohosDislikeCount']
		
	template_vars['reviews'] = Moho.objects.filter(visible=True, like=like).order_by('-id')[:7]

	return render_to_response (
		'moho/reviews.html', 
		template_vars, 
		context_instance=RequestContext(request)
	)
	
def year(request, year):
	template_vars = {}
	
	template_vars['scrollCount'] = Moho.objects.filter(visible=True, year=year).count()
	
	if template_vars['scrollCount']	< 7: 
		template_vars = {
			'disableAJAX': 'true'
		}
	else: 
		template_vars['ajaxType'] = 'year&year={0}'.format(year)
	
	template_vars['reviews'] = Moho.objects.filter(visible=True, year=year).order_by('-id')[:7]

	if template_vars['reviews'].count() == 0: 
		raise Http404
	else: 
		template_vars['title'] = u'Фильмы, снятые в {0}'.format(year)

		return render_to_response (
			'moho/reviews.html', 
			pimp_my_template(template_vars), 
			context_instance=RequestContext(request)
		)
	
def id(request, id):
	template_vars = {
		'disableAJAX': 'true'
	}

	template_vars['reviews'] = Moho.objects.filter(visible=True, id=id)[:1]

	if template_vars['reviews'].count() == 0: 
		raise Http404
	else:
		return HttpResponsePermanentRedirect (
			reverse('mohos.views.slug', args=[str(template_vars['reviews'][0].year), str(template_vars['reviews'][0].slug)])
		)

def slug(request, year, slug):
	template_vars = {
		'disableAJAX': 'true'
	}

	template_vars['reviews'] = Moho.objects.filter(visible=True, year=year, slug=slug)[:1]

	if template_vars['reviews'].count() == 0: 
		raise Http404
	else:
		template_vars['enable_similar'] = True
		template_vars['og_post'] = template_vars['reviews'][0]
		template_vars['title'] = u'Мнение о фильме {0}'.format(template_vars['reviews'][0].title)

		return render_to_response (
			'moho/reviews.html', 
			pimp_my_template(template_vars), 
			context_instance=RequestContext(request)
		)
	
def pimp_my_template(template):
	template['mohosTotalCount'] = Moho.objects.filter(visible=True).count()
	template['mohosLikeCount'] = Moho.objects.filter(like=True, visible=True).count()
	template['mohosDislikeCount'] = template['mohosTotalCount'] - template['mohosLikeCount']

	return template