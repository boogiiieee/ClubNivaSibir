# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import re, os
from pytils.translit import slugify

##################################################################################################	
##################################################################################################

#Анкета пользователя		
class UserProfile(models.Model):
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/user_profile/%d/%s' % (instance.user.id, filename.lower())
	user = models.OneToOneField(User, primary_key=True)
	car = models.CharField(max_length=100, verbose_name=_('You car'), blank=True)
	file = models.FileField(upload_to=make_upload_path, verbose_name=u"фото", blank=True, null=True)
	
	def get_user(self): return self.user
	def get_car(self): return self.car
	
	def __unicode__(self):
		return self.get_user().username
		
	def create_profile_partner(self, city, company, phone, post, dealer_code):
		profile_partner, created = UserProfilePartner.objects.get_or_create(user=self.user, city = city, company = company, phone = phone, post = post, dealer_code = dealer_code)
		return profile_partner
	
	def is_partner(self):
		profile_partner = UserProfilePartner.objects.filter(user=self.user)
		if profile_partner: return True
		else: return False
	
	def get_profile_partner(self):
		profile_partner = UserProfilePartner.objects.get(user=self.user)
		return profile_partner
 
	class Meta: 
		verbose_name = _('profile')
		verbose_name_plural = _('profiles')
		
def create_user_profile(sender, instance, created, **kwargs):  
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)


#Анкета партнера		
class UserProfilePartner(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	city = models.CharField(max_length=100, verbose_name=u'Город')
	company = models.CharField(max_length=500, verbose_name=u'Название компании')
	phone = models.CharField(max_length=100, verbose_name=u'Телефон')
	post = models.CharField(max_length=100, verbose_name=u'Должность', blank=True, null=True)
	dealer_code = models.CharField(max_length=100, verbose_name=u'Код дилера', blank=True, null=True)

	def get_user(self): return self.user
	def get_city(self): return self.city
	
	def __unicode__(self):
		return self.get_user().username
 
	class Meta: 
		verbose_name = u'профайл партнера'
		verbose_name_plural = u'профайлы партнеров'
	
##################################################################################################	
##################################################################################################