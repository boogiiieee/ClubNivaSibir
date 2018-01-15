# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import models as TinymceField
from sorl.thumbnail import ImageField as SorlImageField
from django.core.exceptions import ValidationError
import datetime
import re
import os

##########################################################################
##########################################################################

class NewsArticleManager(models.Manager): 
	def get_query_set(self): 
		return super(NewsArticleManager, self).get_query_set().filter(is_active=True) 

class NewsArticle(models.Model):
	def make_upload_path(instance, filename):
		return u'upload/news/%s' % filename.lower()
		
	title = models.CharField(max_length=100, verbose_name=_("title"))
	image = SorlImageField(upload_to=make_upload_path, verbose_name=_("image"), blank=True, null=True)
	announcement = models.TextField(max_length=500, verbose_name=_("announcement"))
	text = models.TextField(max_length=100000, verbose_name=_("text"))
	created_at = models.DateTimeField(verbose_name = _("date_created"))
	is_active = models.BooleanField(verbose_name=_("is_active"), default=True)
	sort = models.IntegerField(verbose_name=_("order"), default=0)
	
	description = models.TextField(_('description'), blank=True)
	keywords = models.TextField(_('keywords'), blank=True)
	
	objects = models.Manager()
	activs = NewsArticleManager()
	
	def get_title(self): return self.title
	def get_image(self): return self.image
	def get_announcement(self): return self.announcement
	def get_text(self): return self.text
	def get_created_at(self): return self.created_at
	def get_description(self): return self.description
	def get_keywords(self): return self.keywords
	
	def __unicode__(self):
		return self.get_title()
		
	@models.permalink
	def get_absolute_url(self):
		return ('news_url', (), {})
		
	@models.permalink
	def get_item_url(self):
		return ('news_item_url', (), {'id': self.id})
		
	def clean(self):
		r = re.compile('^([a-zA-Z0-9_-]+)\.(jpg|jpeg|png|bmp|gif)$', re.IGNORECASE)
		if self.get_image():
			if not r.findall(os.path.split(self.get_image().url)[1]):
				raise ValidationError(_("File name validation error."))
		
	class Meta: 
		verbose_name = _("news_article")
		verbose_name_plural = _("news")
		ordering = ['sort', '-created_at']
		
##########################################################################
##########################################################################