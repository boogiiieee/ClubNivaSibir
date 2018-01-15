# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField as SorlImageField
from django.core.exceptions import ValidationError
import datetime
import re
import os

##########################################################################
##########################################################################

class UserPhoto(models.Model):
	def make_upload_path(instance, filename):
		return u'upload/userphoto/%s' % filename.lower()
		
	username = models.CharField(max_length=100, verbose_name=_("username"))
	image = SorlImageField(upload_to=make_upload_path, verbose_name=_("photo"), blank=True, null=True)
	text = models.TextField(max_length=2000, verbose_name=_("text"), blank=True)
	phone = models.CharField(max_length=100, verbose_name=_("phone"), blank=True)
	email = models.CharField(max_length=100, verbose_name=_("email"), blank=True)
	created_at = models.DateTimeField(verbose_name = _("date created"), auto_now_add=True)
	is_active = models.BooleanField(verbose_name=_("is active"), default=True)
	sort = models.IntegerField(verbose_name=_("order"), default=0)
	
	def get_username(self): return self.username
	def get_image(self): return self.image
	def get_text(self): return self.text
	def get_phone(self): return self.phone
	def get_email(self): return self.email
	def get_created_at(self): return self.created_at
	
	def __unicode__(self):
		return self.get_username()
		
	def clean(self):
		r = re.compile('^([a-zA-Z0-9_-]+)\.([a-zA-Z0-9_-]+)$')
		if self.image:
			if not r.findall(os.path.split(self.image.url)[1]):
				raise ValidationError(_("File name validation error"))
		
	class Meta: 
		verbose_name = _("user photo")
		verbose_name_plural = _("users photos")
		ordering = ['sort', '-created_at']
		
##########################################################################
##########################################################################