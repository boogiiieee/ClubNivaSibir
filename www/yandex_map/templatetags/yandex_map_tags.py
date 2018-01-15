# -*- coding: utf-8 -*-

from django import template
from django.template import Node, NodeList, Template, Context, Variable
from django.template import TemplateSyntaxError
from django.template import get_library, Library, InvalidTemplateLibrary
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
import settings
import os
import re

register = template.Library()

#######################################################################################################################
#######################################################################################################################

#Выводит карту
class GetYandexMapNode(Node):
	def __init__(self, id):
		self.id = id

	def render(self, context):
		from yandex_map.models import Map
		try:
			item = Map.activs.get(id=int(self.id))
			return render_to_response('yandex_map.html', {'item':item})._get_content()
		except: return u''
		
def get_yandex_map(parser, token):
	bits = token.split_contents()
	if len(bits) != 2: raise TemplateSyntaxError(_("Error token tag \"get_yandex_map\""))
	return GetYandexMapNode(bits[1])
	
get_yandex_map = register.tag(get_yandex_map)

#######################################################################################################################
#######################################################################################################################