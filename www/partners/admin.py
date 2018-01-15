# -*- coding: utf-8 -*-

from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from partners.models import Partner

class PartnerAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('title', 'site', 'is_active', 'sort')
	list_filter = ('is_active',)
	list_editable = ('is_active', 'sort')
 
admin.site.register(Partner, PartnerAdmin)