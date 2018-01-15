# -*- coding: utf-8 -*-

from django.template.base import Node, NodeList, Template, Context, Variable
from django import template
import re

from banners.models import Banner

register = template.Library()

################################################################################################################
################################################################################################################

class GetBannersListNode(Node):
	def render(self, context):
		context['banners_list'] = Banner.activs.all()
		return ''
		
def get_banners_list(parser, token):
	bits = list(token.split_contents())
	if len(bits) != 1: raise TemplateSyntaxError("%r take > 1 argument" % bits[0])
	return GetBannersListNode()
	
get_banners_list = register.tag(get_banners_list)

################################################################################################################
################################################################################################################