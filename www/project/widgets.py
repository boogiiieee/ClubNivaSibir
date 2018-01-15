# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from sorl.thumbnail.fields import ImageField, ImageFormField
from sorl.thumbnail.shortcuts import get_thumbnail

class ImageWidget(forms.ClearableFileInput):
	clear_checkbox_label = u'Удалить изображение'
	
	template_with_initial = u'%(clear_template)s %(input_text)s: %(input)s'
	template_with_clear = u'<label class="checkbox">%(clear)s %(clear_checkbox_label)s</label>'

	def render(self, name, value, attrs=None):
		output = super(ImageWidget, self).render(name, value, attrs)
		if value and hasattr(value, 'url'):
			try: mini = get_thumbnail(value, 'x80', upscale=False)
			except Exception: pass
			else:
				output = (
					u'<div style="float:left">'
					u'<a style="width:%spx;display:block;margin:0 0 10px" class="thumbnail" target="_blank" href="%s">'
					u'<img src="%s"></a>%s</div>'
				) % (mini.width, value.url, mini.url, output)
		return mark_safe(output)