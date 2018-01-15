# -*- coding: utf-8 -*-

from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode

from like.models import Like

register = template.Library()

##########################################################################
##########################################################################

class RenderLikeNode(template.Node):
	def handle_token(cls, parser, token):
		tokens = token.contents.split()
		if tokens[1] != 'for':
			raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

		if len(tokens) == 4:
			return cls(
				object_expr = parser.compile_filter(tokens[2]),
				name = tokens[3],
			)
		else:
			raise template.TemplateSyntaxError("%r tag requires 3 arguments" % tokens[0])

	handle_token = classmethod(handle_token)

	def __init__(self, object_expr=None, name=None):
		if object_expr is None and name is None:
			raise template.TemplateSyntaxError("Like nodes must be given either a literal object.")

		self.object_expr = object_expr
		self.name = template.Variable(name)

	def get_like(self, context):
		ctype, object_pk = self.get_target_ctype_pk(context)
		if ctype and object_pk:
			try:
				obj = Like.objects.get_or_create(
					content_type = ctype,
					object_pk = smart_unicode(object_pk),
				)[0]
			except:
				return None
			else:
				return obj
		return None

	def get_target_ctype_pk(self, context):
		if self.object_expr:
			try:
				obj = self.object_expr.resolve(context)
			except template.VariableDoesNotExist:
				return None, None
			return ContentType.objects.get_for_model(obj), obj.pk
		else:
			return None, None

	def render(self, context):
		ctype, object_pk = self.get_target_ctype_pk(context)
		if object_pk:
			template_search_list = [
				"like/%s/%s/like.html" % (ctype.app_label, ctype.model),
				"like/%s/like.html" % ctype.app_label,
				"like/like.html"
			]
			obj = self.get_like(context)
			liststr = render_to_string(template_search_list, {
				'obj': obj,
				'ctype': ctype,
				'object_pk': object_pk,
				'name': self.name.resolve(context),
			}, context)
			return liststr
		else:
			return ''
			
##########################################################################
##########################################################################

def render_like(parser, token):
	"""
	Syntax::
		{% render_like for [object] %}

	Example usage::
		{% render_like for event %}

	"""
	return RenderLikeNode.handle_token(parser, token)

register.tag(render_like)

##########################################################################
##########################################################################
