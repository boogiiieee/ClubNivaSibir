# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError
import re

from forum.models import Post, AttachFile
from markitup.widgets import AdminMarkItUpWidget

##########################################################################
##########################################################################

class CreateThreadForm(forms.Form):
	title = forms.CharField(label=_("Title"), max_length=100, widget=TextInput(attrs={'placeholder':_('Title'), 'required':True}))
	body = forms.CharField(label=_("Body"), widget=AdminMarkItUpWidget(attrs={'rows':8, 'cols':50, 'placeholder':_('Body'), 'required':True}))
	subscribe = forms.BooleanField(label=_("Subscribe via email"), required=False)

##########################################################################
##########################################################################

class ReplyForm(forms.Form):
	body = forms.CharField(label=_("Body"), widget=AdminMarkItUpWidget(attrs={'rows':8, 'cols':50, 'placeholder':_('Body'), 'required':True}))
	subscribe = forms.BooleanField(label=_("Subscribe via email"), required=False)

class PostEditForm(forms.Form):
	body = forms.CharField(label=_("Body"), widget=AdminMarkItUpWidget(attrs={'rows':8, 'cols':50, 'placeholder':_('Body'), 'required':True}))
	class Meta:
		model = Post
		fields = ('body',)
	
class AttachFileForm(forms.ModelForm):
	class Meta:
		model = AttachFile
		fields = ('file',)
		
	def clean_file(self): 
		file = self.cleaned_data['file']
		r = re.compile('^(.+)\.(png|gif|jpg|jpeg|bmp)$', re.IGNORECASE)
		if file:
			if file._size > 1024*1024:
				raise ValidationError(u"Размер файла более 10Мб")
		return file 

class AttachFileFormset(inlineformset_factory(Post, AttachFile, form=AttachFileForm, can_delete=True, extra=5)):
	pass
	
##########################################################################
##########################################################################

