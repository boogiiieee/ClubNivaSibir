# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField as SorlImageField
from django.core.exceptions import ValidationError
import re
import os

################################################################################################################
################################################################################################################

class BannerManager(models.Manager): 
	def get_query_set(self): 
		return super(BannerManager, self).get_query_set().filter(is_active=True) 

class Banner(models.Model):
	def make_upload_path(instance, filename):
		return u'upload/banners/%s' % filename.lower()
		
	title = models.CharField(max_length=100, verbose_name=_("title"))
	image = SorlImageField(upload_to=make_upload_path, verbose_name=_("image"), help_text=_("help text banner image"))
	url = models.URLField(verbose_name=_("url"), help_text=_("help text banner url"), blank=True)
	description = models.TextField(max_length=1000, verbose_name=_("description"), blank=True)
	is_active = models.BooleanField(verbose_name=_("is_active"), default=True)
	sort = models.IntegerField(verbose_name=_("order"), default=0)
	
	objects = models.Manager()
	activs = BannerManager()
	
	def get_title(self): return self.title
	def get_image(self): return self.image
	def get_url(self): return self.url
	def get_description(self): return self.description
          
	def __unicode__(self):
		return self.get_title()
		
	def clean(self):
		r = re.compile('^([a-zA-Z0-9_-]+)\.(jpg|jpeg|png|bmp|gif)$', re.IGNORECASE)
		if self.get_image():
			if not r.findall(os.path.split(self.get_image().url)[1]):
				raise ValidationError(_("File name validation error."))
     
	class Meta:
		verbose_name = _("banner")
		verbose_name_plural = _("banners")
		ordering = ['sort', '-id']
		
################################################################################################################
################################################################################################################