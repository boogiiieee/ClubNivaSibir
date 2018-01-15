# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import models as TinymceField

################################################################################################################
################################################################################################################

class MapManager(models.Manager): 
	def get_query_set(self): 
		return super(MapManager, self).get_query_set().filter(is_active=True)

class Map(models.Model):
	title = models.CharField(max_length=100, verbose_name=_("title"))
	fid = models.CharField(max_length=100, verbose_name=_("fid"))
	text = TinymceField.HTMLField(max_length=500, verbose_name=_("text"))
	
	width = models.IntegerField(verbose_name=_("width px"))
	height = models.IntegerField(verbose_name=_("height px"))
	
	map_x = models.CharField(max_length=100, verbose_name=_("map coord x"))
	map_y = models.CharField(max_length=100, verbose_name=_("map coord y"))
	placemark_x = models.CharField(max_length=100, verbose_name=_("placemark coord x"))
	placemark_y = models.CharField(max_length=100, verbose_name=_("placemark coord y"))
	zoom = models.IntegerField(verbose_name=_("zoom"))
	
	is_active = models.BooleanField(verbose_name=_("is_active"), default=True)
	sort = models.IntegerField(verbose_name=_("order"), default=0)
	
	objects = models.Manager()
	activs = MapManager()
	
	def __unicode__(self):
		return self.title
     
	class Meta:
		verbose_name = _("map")
		verbose_name_plural = _("maps")
		ordering = ['sort', '-id']
		
################################################################################################################
################################################################################################################