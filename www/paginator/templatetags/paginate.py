# -*- coding: utf-8 -*-

from django.template.base import Node, NodeList, Template, Context, Variable
from django import template
import re

register = template.Library()

#######################################################################################################################
#######################################################################################################################

class paginate_split_list_node(Node):
	def __init__(self, page_range, page):
		self.page_range = template.Variable(page_range)
		self.page = template.Variable(page)

	def render(self, context):
		page_range = self.page_range.resolve(context)
		page = self.page.resolve(context)
		page_count = len(page_range)
		
		prev1, next1 = False, False
		if page > 1: prev1 = page - 1
		if page < page_count: next1 = page + 1
		
		if page_count > 10:
			if page < 5 or page > page_count-4:
				new_page_range = [[page_range[:5],True], [page_range[-5:],False]]
			else:
				new_page_range = [[page_range[:3],True], [page_range[page-2:page+1],True], [page_range[-3:],False]]
		else:
			new_page_range = [[page_range],False]
		
		context['paginate_page_range'] = [new_page_range, prev1, next1]
		return ''
		
def paginate_split_list(parser, token):
	bits = list(token.split_contents())
	if len(bits) != 3:
		raise TemplateSyntaxError("%r takes < 3 arguments" % bits[0])
	return paginate_split_list_node(bits[1], bits[2])
	
paginate_split_list = register.tag(paginate_split_list)

#######################################################################################################################
#######################################################################################################################

class get_url_node(Node):
	def __init__(self, opt, val, com, v):
		self.opt = opt
		self.val = val
		
		self.com = com
		self.v = v

	def render(self, context):
		g = context['request'].GET
		u = g.urlencode()
		
		if self.com == 'delete-key' and self.v:
			if u:
				e = g.copy()
				if self.v in e.keys():
					del e[self.v]
					g = e
					
		u = g.urlencode()
		
		try:
			val = template.Variable(self.val).resolve(context)
			if val == 'none':
				if u:
					e = g.copy()
					if self.opt in u: del e[self.opt]
					return u'?%s' % e.urlencode()
				else: return u''
		except: val = self.val
			
		if u:
			if self.opt in u:
				if val == g.get(self.opt): return u'?%s' % u
				else:
					e = g.copy()
					e[self.opt] = val
					return u'?%s' % e.urlencode()
			else: return u'?%s&%s=%s' % (u, self.opt, val)
		else: return u'?%s=%s' % (self.opt, val)
		
def get_url(parser, token):
	bits = token.split_contents()
	if len(bits) < 3:
		raise TemplateSyntaxError(_('Error token tag "get_url"'))
		
	try:
		com = bits[3][1:-1]
		var = bits[4]
	except:
		com = None
		var = None
		
	return get_url_node(bits[1][1:-1], bits[2], com, var)
	
get_url = register.tag(get_url)

#######################################################################################################################
#######################################################################################################################