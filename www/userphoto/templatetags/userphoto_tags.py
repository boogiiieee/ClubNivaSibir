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

class GetUserPhotoNode(Node):
	def __init__(self, var_name):
		self.var_name = var_name

	def render(self, context):
		from userphoto.models import UserPhoto
		context[self.var_name] = UserPhoto.objects.filter(is_active=True)
		return u''
		
def get_userphoto(parser, token):
	bits = token.split_contents()
	if len(bits) != 2: raise TemplateSyntaxError(_("Error token tag \"get_userphoto\""))
	return GetUserPhotoNode(bits[1][1:-1])
	
get_userphoto = register.tag(get_userphoto)

#######################################################################################################################
#######################################################################################################################

class GetUserPhoto1Node(Node):
	def __init__(self, var_name):
		self.var_name = var_name

	def render(self, context):
		from userphoto.models import UserPhoto
		try:
			context[self.var_name] = UserPhoto.objects.get(id=1)
		except:
			context[self.var_name] = UserPhoto.objects.filter(is_active=True)[0]
		return u''
		
def get_userphoto1(parser, token):
	bits = token.split_contents()
	if len(bits) != 2: raise TemplateSyntaxError(_("Error token tag \"get_userphoto1\""))
	return GetUserPhoto1Node(bits[1][1:-1])
	
get_userphoto1 = register.tag(get_userphoto1)

#######################################################################################################################
#######################################################################################################################