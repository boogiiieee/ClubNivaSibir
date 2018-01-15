from django.conf.urls.defaults import *

urlpatterns = patterns('gallery.views',
	url(r'^$', 'all', name='gallery_url'),	
	url(r'^(?P<id>[0-9]{1,4})/$', 'full', name='gallery_item_url'),
)