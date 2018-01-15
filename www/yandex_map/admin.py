# -*- coding: utf-8 -*-

from django.contrib import admin
import settings

from yandex_map.models import Map

##########################################################################
##########################################################################

class MapAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'sort')
	list_filter = ('is_active',)
	list_editable = ('is_active', 'sort')
	
	def has_add_permission(self, *args, **kwargs):
		if not settings.DEBUG: return False
		return super(MapAdmin, self).has_add_permission(*args, **kwargs)
		
	def has_delete_permission(self, *args, **kwargs):
		if not settings.DEBUG: return False
		return super(MapAdmin, self).has_delete_permission(*args, **kwargs)
 
admin.site.register(Map, MapAdmin)

##########################################################################
##########################################################################