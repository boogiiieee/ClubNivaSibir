# -*- coding: utf-8 -*-

from django import forms

from markitup.widgets import AdminMarkItUpWidget

from user_msg.models import Message

##########################################################################
##########################################################################

#Форма сообщений
class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('text',)
		widgets = {
			'text': AdminMarkItUpWidget(attrs={'rows':8, 'cols':50})
		}
		
##########################################################################
##########################################################################