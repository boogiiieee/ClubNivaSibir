# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail.shortcuts import get_thumbnail, delete

from userphoto.models import UserPhoto

##########################################################################
##########################################################################

class UserPhotoAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('username', 'created_at', 'get_thumbnail_image', 'is_active', 'sort')
	list_filter = ('is_active', 'created_at')
	list_editable = ('is_active', 'sort')
	
	def get_thumbnail_image(self, obj):
		image = obj.get_image()
		if image:
			f = get_thumbnail(image, '50x50', crop='center', quality=99, format='PNG')
			return '<img src="%s" />' % f.url
		return '<img src="/media/img/no_image_50x50.png" />'
	get_thumbnail_image.short_description = _("Image")
	get_thumbnail_image.allow_tags = True
	
admin.site.register(UserPhoto, UserPhotoAdmin)

##########################################################################
##########################################################################