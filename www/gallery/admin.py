# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail.shortcuts import get_thumbnail, delete

from gallery.models import CategoryGallery, PhotoGallery

##########################################################################
##########################################################################

class PhotoGalleryInline(AdminImageMixin, admin.StackedInline):
	model = PhotoGallery

class CategoryGalleryAdmin(AdminImageMixin, admin.ModelAdmin):
	inlines = [PhotoGalleryInline]
	list_display = ('title', 'date', 'is_active', 'order')
	list_filter = ('is_active', 'date')
	list_editable = ('is_active', 'order')
	readonly_fields = ('get_thumbnail_image',)
	
	fieldsets = (
		(None, {'fields': ('title', 'date', 'is_active', 'order')},),
		(_('Meta tags'), {'classes': ('collapse',), 'fields': ('description', 'keywords')}),
	)
	
	def get_thumbnail_image(self, obj):
		image = obj.get_image()
		if image:
			image = image.get_image()
			if image:
				f = get_thumbnail(image, '50x50', crop='center', quality=99, format='PNG')
				return '<img src="%s" />' % f.url
		return '<img src="/media/img/no_image_50x50.png" />'
	get_thumbnail_image.short_description = _("Image")
	get_thumbnail_image.allow_tags = True
 
admin.site.register(CategoryGallery, CategoryGalleryAdmin)

##########################################################################
##########################################################################