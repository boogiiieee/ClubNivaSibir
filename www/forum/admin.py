# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail.shortcuts import get_thumbnail, delete
from forum.models import Forum, Thread, Post, AttachFile, Subscription

##########################################################################
##########################################################################

class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', '_parents_repr', 'for_partner')
    list_filter = ('groups', 'for_partner')
    list_editable = ('for_partner', )
    ordering = ['ordering', 'parent', 'title']
    prepopulated_fields = {"slug": ("title",)}
	
admin.site.register(Forum, ForumAdmin)
	
##########################################################################
##########################################################################

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['author','thread']
	
admin.site.register(Subscription, SubscriptionAdmin)
	
##########################################################################
##########################################################################

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'latest_post_time')
    list_filter = ('forum',)
	
admin.site.register(Thread, ThreadAdmin)
	
##########################################################################
##########################################################################

class AttachFileInline(admin.TabularInline):
	model = AttachFile
	
class PostAdmin(admin.ModelAdmin):
	inlines = [AttachFileInline]
	list_display = ('id', 'thread', 'author', 'time')
	
admin.site.register(Post, PostAdmin)

class AttachFileAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('get_thumbnail_image', 'is_new', 'is_active')
	list_filter = ('is_new', 'is_active')
	list_editable = ('is_new', 'is_active')
	
	def get_thumbnail_image(self, obj):
		if obj.file:
			f = get_thumbnail(obj.file, '50x50', crop='center', quality=99, format='PNG')
			return '<img src="%s" />' % f.url
		return '<img src="/media/img/no_image_50x50.png" />'
	get_thumbnail_image.short_description = _("Image")
	get_thumbnail_image.allow_tags = True
	
admin.site.register(AttachFile, AttachFileAdmin)

##########################################################################
##########################################################################