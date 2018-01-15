# -*- coding: utf-8 -*-

from user_msg.models import Message

##################################################################################################	
##################################################################################################

def custom_proc(request):
	if request.user and request.user.is_authenticated():
		count_new_messages = request.user.get_count_messages()
	else:
		count_new_messages = None
	
	return {
		'count_new_messages': count_new_messages
	}
	
##################################################################################################	
##################################################################################################
