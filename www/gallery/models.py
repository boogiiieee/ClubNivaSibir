# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField as SorlImageField
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
import re
import os

##########################################################################
##########################################################################

class CategoryGalleryManager(models.Manager): 
	def get_query_set(self): 
		return super(CategoryGalleryManager, self).get_query_set().filter(is_active=True) 

class CategoryGallery(models.Model):
	title = models.CharField(max_length=100, verbose_name=_("title"))
	date = models.DateTimeField(verbose_name=_("date"))
	is_active = models.BooleanField(verbose_name=_("is active"), default=True)
	order = models.IntegerField(verbose_name=_("order"), default=0)
	
	description = models.TextField(_('description'), blank=True)
	keywords = models.TextField(_('keywords'), blank=True)
	
	objects = models.Manager()
	activs = CategoryGalleryManager()
	
	def get_title(self): return self.title
	def get_date(self): return self.date
	def get_description(self): return self.description
	def get_keywords(self): return self.keywords
	
	def __unicode__(self):
		return self.get_title()
		
	@models.permalink
	def get_absolute_url(self):
		return ('gallery_url', (), {})
		
	@models.permalink
	def get_item_url(self):
		return ('gallery_item_url', (), {'id':self.id})
		
	def get_image(self):
		imgs = self.gallery_photos.filter(is_main=True, is_active=True)
		if imgs.count(): return imgs[0]
		else:
			imgs = self.gallery_photos.filter(is_active=True)
			if imgs.count(): return imgs.order_by('?')[0]
		return None
		
	def get_images(self):
		return self.gallery_photos.filter(is_active=True)
		
	class Meta:
		verbose_name = _("gallery category")
		verbose_name_plural = _("gallery categorys")
		ordering = ['order', '-id']
	
##########################################################################
##########################################################################

class PhotoGalleryManager(models.Manager): 
	def get_query_set(self): 
		return super(PhotoGalleryManager, self).get_query_set().filter(is_active=True) 
		
class PhotoGallery(models.Model):
	def make_upload_path(instance, filename):
		return u'upload/gallery/%s' % filename.lower()
		
	category = models.ForeignKey(CategoryGallery, verbose_name=_("category"), related_name='gallery_photos')
	title = models.CharField(max_length=100, verbose_name=_("title"))
	image = SorlImageField(upload_to=make_upload_path, verbose_name=_("image"))
	is_main = models.BooleanField(verbose_name=_("is main"), default=False)
	is_active = models.BooleanField(verbose_name=_("is active"), default=True)
	order = models.IntegerField(verbose_name=_("order"), default=0)
	
	objects = models.Manager()
	activs = PhotoGalleryManager()
	
	def get_title(self): return self.title
	def get_image(self): return self.image
          
	def __unicode__(self):
		return self.get_title()
		
	def clean(self,*args, **kwargs):
		r = re.compile('^([a-zA-Z0-9_-]+)\.(jpg|jpeg|png|bmp|gif)$', re.IGNORECASE)
		if self.get_image():
			if not r.findall(os.path.split(self.get_image().url)[1]):
				raise ValidationError(_("File name validation error."))

		file = self.image
		if file.size > 2621440:
			raise ValidationError(u'Загруженный файл слишком велик - %s. Уменьшите изображение перед загрузкой. Допустимый размер файла до 2.5 МБ' % filesizeformat(file.size))


				
	def save(self, *args, **kwargs):
		if self.is_main:
			PhotoGallery.objects.filter(category=self.category, is_main=True).update(is_main=False)
		super(PhotoGallery, self).save(*args, **kwargs)
     
	class Meta:
		verbose_name = _("gallery photo")
		verbose_name_plural = _("gallery photos")
		ordering = ['order', '-id']
		
##########################################################################
##########################################################################