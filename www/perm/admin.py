# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from perm.forms import PermGroupAdminForm, PermUserAdminForm

##########################################################################
##########################################################################

class GroupAdmin(admin.ModelAdmin):
	form = PermGroupAdminForm
	search_fields = ('name',)
	ordering = ('name',)
 
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

##########################################################################
##########################################################################

from project.admin import UserProfileInline, UserProfilePartnerInline

class UserAdmin(UserAdmin):
	inlines = [UserProfileInline, UserProfilePartnerInline]
	form = PermUserAdminForm
	filter_horizontal = ('groups',)
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
	)
 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

##########################################################################
##########################################################################