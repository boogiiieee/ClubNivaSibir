from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
	url(r'^$', 'all', name='news_url'),	
	url(r'^(?P<id>[0-9]{1,4})/$', 'full', name='news_item_url'),
)