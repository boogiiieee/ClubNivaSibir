# -*- coding: utf-8 -*-

from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from itertools import chain
import settings

from perm.conf import settings as conf

##################################################################################################	
##################################################################################################

class PermWidget(CheckboxSelectMultiple):
	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = []
		has_id = attrs and 'id' in attrs
		final_attrs = self.build_attrs(attrs, name=name)
		output = [u'<ul id="id_permissions_ul">']
		str_values = set([force_unicode(v) for v in value])
		app_tmp = None
		for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
			if has_id:
				final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
				label_for = u' for="%s"' % final_attrs['id']
			else: label_for = ''

			cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
			option_value = force_unicode(option_value)
			rendered_cb = cb.render(name, option_value)
			option_label = conditional_escape(force_unicode(option_label))
			
			app, model, can = [i.strip() for i in option_label.split('|')]
			
			if conf.APPS.has_key(app) and conf.APPS[app] and model in conf.APPS[app]:
				for ch in [u' ', u'_', u'-']:
					app = app.split(ch)
					app = ch.join([i[0].upper() + i[1:] for i in app])
					app = _(app)
				can_name, can_obj = can.split(' ')[:2], can.split(' ')[2:]
				can_name = u' '.join(can_name)
				can_obj = u' '.join(can_obj)

				if not app_tmp: output.append(u'<li><label for="id_app_%(app)s">%(app)s</label><ul id="id_app_%(app)s">' % {'app':app})
				elif app_tmp and app_tmp != app: output.append(u'</ul></li><li><label for="id_app_%(app)s">%(app)s</label><ul>' % {'app':app})
				app_tmp = app
				option_label = u'%s %s' % (_(can_name), _(can_obj))
				output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
		output.append(u'</li></ul>')
		return mark_safe(u'\n'.join(output))
		
	def id_for_label(self, id_):
		if id_:
			id_ += '_ul'
		return id_
	id_for_label = classmethod(id_for_label)
	
##################################################################################################	
##################################################################################################