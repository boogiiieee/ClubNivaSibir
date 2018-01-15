# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.forms.widgets import TextInput
from captcha.fields import CaptchaField, CaptchaTextInput
from django.conf import settings

from project.widgets import ImageWidget
from project.models import UserProfile
##################################################################################################	
##################################################################################################

#Профиль пользователя
class ProfileForm(forms.ModelForm):
	car = forms.CharField(max_length=100, label=_('You car'), required=False, widget=TextInput(attrs={'placeholder':_('You car')}))
	file = forms.FileField(required=False, label=u'Ваше фото',widget=ImageWidget())
	def __init__(self, *args, **kw):
		super(ProfileForm, self).__init__(*args, **kw)
		try: 
			self.fields['car'].initial = self.instance.get_profile().car
			self.fields['file'].initial = self.instance.get_profile().file
		except: pass
		
	def save(self, *args, **kw):
		super(ProfileForm, self).save(*args, **kw)
		try: pf = self.instance.get_profile()
		except: pf = UserProfile.objects.get_or_create(user=self.instance)
		else:
			pf.car = self.cleaned_data.get('car')
			if self.cleaned_data.get('file'):
				pf.file = self.cleaned_data.get('file')
			else:
				pf.file = ''
			pf.save()
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')
		widgets = {
			'first_name':TextInput(attrs={'placeholder':_('First name')}),
			'last_name':TextInput(attrs={'placeholder':_('Last name')}),
			'email':TextInput(attrs={'placeholder':_('Email')}),
		}
		
##################################################################################################	
##################################################################################################

#Профиль партнера
class ProfileFormPartner(forms.ModelForm):
	city = forms.CharField(max_length=100, label=u'Город', required=True)
	company = forms.CharField(max_length=100, label=u'Название компании', required=True)
	phone = forms.CharField(max_length=100, label=u'Телефон', required=True)
	post = forms.CharField(max_length=100, label=u'Должность', required=False)
	dealer_code = forms.CharField(max_length=100, label=u'Код дилера', required=False)
	car = forms.CharField(max_length=100, label=_('You car'), required=False, widget=TextInput(attrs={'placeholder':_('You car')}))
	file = forms.FileField(required=False, label=u'Ваше фото',widget=ImageWidget())
	def __init__(self, *args, **kw):
		super(ProfileFormPartner, self).__init__(*args, **kw)
		try: 
			pr = self.instance.get_profile()
			if pr.is_partner():
				prp = pr.get_profile_partner()
				self.fields['city'].initial = prp.city
				self.fields['company'].initial = prp.company
				self.fields['phone'].initial = prp.phone
				self.fields['post'].initial = prp.post
				self.fields['dealer_code'].initial = prp.dealer_code
			self.fields['file'].initial = pr.file
			self.fields['car'].initial = pr.car
		except: pass
		
	def save(self, *args, **kw):
		super(ProfileFormPartner, self).save(*args, **kw)
		try: pf = self.instance.get_profile()
		except: pf = UserProfile.objects.get_or_create(user=self.instance)
		else:
			pf.car = self.cleaned_data.get('car')
			if self.cleaned_data.get('file'):
				pf.file = self.cleaned_data.get('file')
			else:
				pf.file = ''
			pf.save()
		if pf.is_partner():
			pfp = pf.get_profile_partner()
			pfp.city = self.cleaned_data.get('city')
			pfp.company = self.cleaned_data.get('company')
			pfp.phone = self.cleaned_data.get('phone')
			pfp.post = self.cleaned_data.get('post')
			pfp.dealer_code = self.cleaned_data.get('dealer_code')
			pfp.save()
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')
		widgets = {
			'first_name':TextInput(attrs={'placeholder':_('First name')}),
			'last_name':TextInput(attrs={'placeholder':_('Last name')}),
			'email':TextInput(attrs={'placeholder':_('Email')}),
		}

		
##################################################################################################	
##################################################################################################

from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

#Форма регистрации
class RegistrationForm(RegistrationFormUniqueEmail):
	car = forms.CharField(max_length=100, label=_('You car'), required=False)
	captcha = CaptchaField(label=_('Captcha'), widget=CaptchaTextInput(attrs={'placeholder':_('Captcha'), 'required':True}))
	
	def save(self, profile_callback=None):
		new_user = RegistrationProfile.objects.create_inactive_user(
			username=self.cleaned_data['username'],
			password=self.cleaned_data['password1'],
			email=self.cleaned_data['email'],
			profile_callback=profile_callback
		)
		pf = new_user.get_profile()
		pf.car = self.cleaned_data['car']
		pf.save() 

		return new_user

##################################################################################################	
##################################################################################################


#Форма регистрации партнера
class RegistrationFormPartner(RegistrationFormUniqueEmail):
	first_name = forms.CharField(max_length=100, label=u'Имя', required=True)
	last_name = forms.CharField(max_length=100, label=u'Фамилия', required=True)
	city = forms.CharField(max_length=100, label=u'Город', required=True)
	company = forms.CharField(max_length=100, label=u'Название компании', required=True)
	phone = forms.CharField(max_length=100, label=u'Телефон', required=True)
	post = forms.CharField(max_length=100, label=u'Должность', required=False)
	dealer_code = forms.CharField(max_length=100, label=u'Код дилера', required=False)
	car = forms.CharField(max_length=100, label=_('You car'), required=False)
	captcha = CaptchaField(label=_('Captcha'), widget=CaptchaTextInput(attrs={'placeholder':_('Captcha'), 'required':True}))
	
	def save(self, profile_callback=None):
		new_user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password1'])
		new_user.is_active = False
		new_user.first_name = self.cleaned_data['first_name']
		new_user.last_name = self.cleaned_data['last_name']
		new_user.save()
		
		registration_profile = RegistrationProfile.objects.create_profile(new_user)

		if profile_callback is not None:
			profile_callback(user=new_user)

		from django.core.mail import send_mail
		current_site = Site.objects.get_current()
		
		subject = render_to_string('registration/activation_email_subject.txt',
								   { 'site': current_site })

		pf = new_user.get_profile()
		pf.car = self.cleaned_data['car']
		pf.save() 
		pf_partn = pf.create_profile_partner(self.cleaned_data['city'], self.cleaned_data['company'], self.cleaned_data['phone'], self.cleaned_data['post'], self.cleaned_data['dealer_code'])
		
		# Email subject *must not* contain newlines
		subject = ''.join(subject.splitlines())
		
		from threadmail import threading_send_mail
		threading_send_mail('registration/activation_email.html', u'%s' % subject, settings.MANAGERS_FORUM_PARTNER,
			{
				'partner': pf_partn,
				'activation_key': registration_profile.activation_key,
				'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
				'site': current_site,
			}
		)
		return new_user

##################################################################################################	
##################################################################################################