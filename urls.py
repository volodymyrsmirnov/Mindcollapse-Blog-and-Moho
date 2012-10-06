from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'mindcollapse_com.views.home', name='home'),
	# url(r'^mindcollapse_com/', include('mindcollapse_com.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:

	url(r'^godmode/blog_upload_file$', 'blogs.views.upload_file'),
	url(r'^godmode/blog_autosave_post$', 'blogs.views.autosave_post'),
	url(r'^godmode/', include(admin.site.urls)), 
	
	url(r'^moho/$', 'mohos.views.index'), 
	url(r'^moho/(?P<attitude>like|dislike)/$', 'mohos.views.attitude'),
	url(r'^moho/year/(?P<year>\d{4})/$', 'mohos.views.year'),
	url(r'^moho/id/(?P<id>\d+)$', 'mohos.views.id'),
	
	url(r'^moho/genre/(?P<genre>.*)/$', 'mohos.views.genre'),
	url(r'^moho/actor/(?P<actor>.*)/$', 'mohos.views.actor'),
	url(r'^moho/director/(?P<director>.*)/$', 'mohos.views.director'),
	
	url(r'^moho/ajax/$', 'mohos.views.ajax'),
	url(r'^moho/rss\.xml$', 'mohos.views.rss'),
	url(r'^moho/sitemap\.xml$', 'mohos.views.sitemap'),
	
	url(r'^blog/$', 'blogs.views.index'),    
	url(r'^blog/page/(?P<page>\d+)/$', 'blogs.views.index'),
	url(r'^blog/(?P<id>\d+)\.html$', 'blogs.views.id'),
	url(r'^blog/(?P<id>\d+)\.pdf$', 'blogs.views.id_pdf'),
	url(r'^blog\.xml$', 'blogs.views.rss'),
	url(r'^blog/tag/(?P<tag>\w+)/page/(?P<page>\d+)/$', 'blogs.views.tag'),		
	url(r'^blog/tag/(?P<tag>\w+)/$', 'blogs.views.tag'),
	url(r'^blog/sitemap\.xml$', 'blogs.views.sitemap'),
	url(r'^$', 'blogs.views.index'),   
	
)
