# -*- coding: utf-8 -*-

from django.contrib import admin

from like.models import Like

##########################################################################
##########################################################################

class LikeAdmin(admin.ModelAdmin):
	list_display = ('like_count', 'content_type', 'object_pk', 'ip_address', 'created', 'modified')
	list_filter = ('created', 'modified')
	date_hierarchy = 'created'
	ordering = ('-created',)
	search_fields = ('ip_address',)

admin.site.register(Like, LikeAdmin)

##########################################################################
##########################################################################
