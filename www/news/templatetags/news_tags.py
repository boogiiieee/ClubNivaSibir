# -*- coding: utf-8 -*-

from django.template.base import Node, NodeList, Template, Context, Variable
from django import template
import re

from news.models import NewsArticle

register = template.Library()

################################################################################################################
################################################################################################################

class GetNewsListNode(Node):
	def render(self, context):
		context['news_list'] = NewsArticle.activs.all()[:10]
		return ''
		
def get_news_list(parser, token):
	bits = list(token.split_contents())
	if len(bits) != 1: raise TemplateSyntaxError("%r take > 1 argument" % bits[0])
	return GetNewsListNode()
	
get_news_list = register.tag(get_news_list)

################################################################################################################
################################################################################################################