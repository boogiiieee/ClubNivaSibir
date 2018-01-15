# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.core import urlresolvers
from django.conf import settings

##########################################################################
##########################################################################

class BaseLikeAbstractModel(models.Model):
	content_type = models.ForeignKey(ContentType, verbose_name=u'контент', related_name="content_type_set_for_%(class)s")
	object_pk = models.TextField(u'ID объекта')
	content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

	class Meta:
		abstract = True
	
##########################################################################
##########################################################################

class Like(BaseLikeAbstractModel):
	like_count = models.IntegerField(verbose_name=u'количество голосов', default=0)
	ip_address = models.IPAddressField(verbose_name=u'IP адрес', blank=True, null=True)

	created = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	modified = models.DateTimeField(verbose_name=u'дата обновления', auto_now=True)

	class Meta:
		verbose_name = u'рейтинг'
		verbose_name_plural = u'голосование'
		ordering = ('created',)

	def __unicode__(self):
		return u'рейтинг'
		
##########################################################################
##########################################################################

class DoubleProtection(models.Model):
	ip = models.CharField(max_length=20, blank=True)
	count = models.IntegerField(default=0)
	created = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return u'Защита от повторных кликов'
		
##########################################################################
##########################################################################