from django.conf.urls import *

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^instagram/$', 'hipstagram.views.index'), 
	url(r'^instagram/rss\.xml$', 'hipstagram.views.rss'), 

	url(r'^godmode/blog_upload_file$', 'blogs.views.upload_file'),
	url(r'^godmode/blog_autosave_post$', 'blogs.views.autosave_post'),
	url(r'^godmode/', include(admin.site.urls)), 
	
	url(r'^moho/$', 'mohos.views.index'), 
	url(r'^moho/(?P<attitude>like|dislike)/$', 'mohos.views.attitude'),
	url(r'^moho/id/(?P<id>\d+)$', 'mohos.views.id'),
	
	url(r'^moho/genre/(?P<genre>.*)/$', 'mohos.views.genre'),
	url(r'^moho/actor/(?P<actor>.*)/$', 'mohos.views.actor'),
	url(r'^moho/director/(?P<director>.*)/$', 'mohos.views.director'),
	
	url(r'^moho/ajax/$', 'mohos.views.ajax'),
	url(r'^moho/rss\.xml$', 'mohos.views.rss'),
	url(r'^moho/sitemap\.xml$', 'mohos.views.sitemap'),

	url(r'^moho/(?P<year>\d{4})/$', 'mohos.views.year'),
	url(r'^moho/(?P<year>\d{4})/(?P<slug>.*)\.html$', 'mohos.views.slug'),

	url(r'^blog/$', 'blogs.views.index'),   
	url(r'^blog/archive/$', 'blogs.views.archive'),     
	url(r'^blog/(?P<id>\d+)\.html$', 'blogs.views.id'),
	url(r'^blog/(?P<slug>.*)\.html$', 'blogs.views.slug'),
	url(r'^blog\.xml$', 'blogs.views.rss'),
	url(r'^blog/sitemap\.xml$', 'blogs.views.sitemap'),
	url(r'^$', 'blogs.views.index'),	
)
