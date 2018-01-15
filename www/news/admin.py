# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin

from news.models import NewsArticle

##########################################################################
##########################################################################

class NewsArticleAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('title', 'created_at', 'is_active', 'sort')
	list_filter = ('is_active', 'created_at')
	list_editable = ('is_active', 'sort')
	fieldsets = (
		(None, {'fields': ('title', 'image', 'announcement', 'text', 'created_at', 'is_active', 'sort')},),
		(_('Meta tags'), {'classes': ('collapse',), 'fields': ('description', 'keywords')}),
	)
	
admin.site.register(NewsArticle, NewsArticleAdmin)

##########################################################################
##########################################################################