from django.conf.urls.defaults import *

urlpatterns = patterns('like.views',
	url(r'^$', 'add_like', name='add_like_url'),	
)