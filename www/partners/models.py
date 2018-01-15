# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField as SorlImageField
from django.core.exceptions import ValidationError
import re
import os

class Partner(models.Model):
	def make_upload_path(instance, filename):
		return u'upload/partners/%s' % filename.lower()
	title = models.CharField(max_length=100, verbose_name=u"заголовок")
	image = SorlImageField(upload_to=make_upload_path, verbose_name=u"изображение", help_text=u'рекомендованный размер изображения 400x250px')
	site = models.URLField(verbose_name=u"сайт", help_text=u"ссылка на сайт партнеров", blank=True)
	is_active = models.BooleanField(verbose_name=u"активно", default=True)
	sort = models.IntegerField(verbose_name=u"порядок", default=0)
          
	def __unicode__(self):
		return u'%s' % self.title
		
	def get_title(self):self.title
	def get_image(self):self.image
	def clean(self):
		r = re.compile('^([a-zA-Z0-9_-]+)\.(jpg|jpeg|png|bmp|gif)$', re.IGNORECASE)
		if self.image:
			if not r.findall(os.path.split(self.image.url)[1]):
				raise ValidationError(u"Неккоректное имя файла.")
     
	class Meta:
		verbose_name = u"партнер"
		verbose_name_plural = u"партнеры"
		ordering = ['sort', '-id'] 