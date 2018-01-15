# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm

from perm.widgets import PermWidget

##################################################################################################	
##################################################################################################

class PermGroupAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PermGroupAdminForm, self).__init__(*args, **kwargs)
		self.fields['permissions'].help_text = ''
		
	class Meta:
		model = Group
		fields = ('name', 'permissions')
		widgets = {
			'permissions': PermWidget(),
		}
		
##################################################################################################	
##################################################################################################

class PermUserAdminForm(UserChangeForm):
	def __init__(self, *args, **kwargs):
		super(PermUserAdminForm, self).__init__(*args, **kwargs)
		self.fields['user_permissions'].help_text = ''
		
	class Meta:
		model = User
		widgets = {
			'user_permissions': PermWidget(),
		}
		
##################################################################################################	
##################################################################################################