# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

#######################################################################################################################
#######################################################################################################################

#Настройки
class ConfigModel(models.Model):
	site_name = models.CharField(max_length=100, verbose_name=_("site name"))

	def __unicode__(self):
		return u'%s' % _("configuration")
		
	class Meta: 
		verbose_name = _("configuration") 
		verbose_name_plural = _("configurations")
		
	def get_site_name(self): return self.site_name
		
#######################################################################################################################
#######################################################################################################################