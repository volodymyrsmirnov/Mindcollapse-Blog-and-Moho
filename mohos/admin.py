from mohos.models import Moho, Actor, Genre, Director
from django.contrib import admin

from django import forms
from django.db import models

class SubMohoAdmin(admin.ModelAdmin):

	save_on_top = True
	list_per_page = 50
	
	prepopulated_fields = {"slug": ("name",)}
	
	def titlezed(obj):
		return obj.name.title()
		
	def countFilms(obj):
		if type(obj) == Genre:
			return Moho.objects.filter(genres__slug=obj.slug).count()
		elif type(obj) == Actor:
			return Moho.objects.filter(actors__slug=obj.slug).count()
		elif type(obj) == Director:
			return Moho.objects.filter(directors__slug=obj.slug).count()
		else:
			return 0 		
	titlezed.short_description = 'Name'
	countFilms.short_description = 'Attached to films'
	
	list_display = ('id', titlezed, countFilms)
	
	search_fields = ['name']

class MohoAdmin(admin.ModelAdmin):

	#formfield_overrides = {
	#	models.Field: {'widget': forms.TextInput},
	#}

	list_display = ('id', 'title', 'year', 'like', 'visible')
	list_filter = ('like','visible', 'genres')
	
	fieldsets = (
	
		(None, {
			'fields': ('title', 'text', 'visible', 'like', )
		}),
		
		('Film details', {
			'fields': ('year', 'imageURL', 'imdbURL', 'directors', 'actors', 'genres')
		}),
		
	)
	
	filter_horizontal = ['directors', 'actors', 'genres']
	
	list_per_page = 50
	save_on_top = True
	search_fields = ['title', 'text']
	
	class Media:
			css = {
				"all": ("/admin/general.css", "/admin/cleditor/jquery.cleditor.css")
			}
			js = ("https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js", "/admin/cleditor/jquery.cleditor.js", "/admin/general.js")
	
admin.site.register(Moho, MohoAdmin)
admin.site.register(Actor, SubMohoAdmin)
admin.site.register(Genre, SubMohoAdmin)
admin.site.register(Director, SubMohoAdmin)
