from django.conf.urls.defaults import *

urlpatterns = patterns('user_msg.views',
	url(r'^careate/$', 'user_msg_careate', name='user_msg_careate'),	
	url(r'^dialog/$', 'user_msg_dialog', name='user_msg_dialog'),
	url(r'^dialog/(?P<dialog_id>[0-9]+)/$', 'user_msg_messages', name='user_msg_messages'),
)