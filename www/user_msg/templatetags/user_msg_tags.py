# -*- coding: utf-8 -*-

from django import template
register = template.Library()

##################################################################################################	
##################################################################################################

@register.filter(name='get_last_messages_from_user')
def get_last_messages_from_user(user, from_user):
	return user.get_last_messages(from_user)

@register.filter(name='count_messages_from_user')
def count_messages_from_user(user, from_user):
	return user.get_count_messages(from_user)
	
##################################################################################################	
##################################################################################################