# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sorl.thumbnail.admin import AdminImageMixin
from django.contrib.auth.models import User

from project.models import UserProfile, UserProfilePartner

##############################################################################################
##############################################################################################

#Анкета пользователя	
class UserProfileInline(admin.StackedInline):
	model = UserProfile
	fk_name = 'user'
	max_num = 1
	
#Анкета партнера	
class UserProfilePartnerInline(admin.StackedInline):
	model = UserProfilePartner
	fk_name = 'user'
	max_num = 1
    
class CustomUserAdmin(UserAdmin):
	inlines = [UserProfileInline, UserProfilePartnerInline]

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

##############################################################################################
##############################################################################################