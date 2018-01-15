# -*- coding: utf-8 -*-

from django.template import loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
import settings

from project.forms import ProfileForm, ProfileFormPartner

##########################################################################
##########################################################################

@login_required
def profile_change_password(request):
	if request.method == 'POST':
		form2 = PasswordChangeForm(user=request.user, data=request.POST)
		if form2.is_valid():
			form2.save()
			messages.add_message(request, messages.INFO, 'Пароль успешно изменен.')
			return HttpResponseRedirect('/accounts/profile/')
	messages.add_message(request, messages.ERROR, 'Ошибка изменения пароля!')
	return HttpResponseRedirect('/accounts/profile/')

##########################################################################
##########################################################################

@login_required
def profile_views(request):
	partner=False
	if request.user.get_profile().is_partner():
		partner=True
	if request.method == 'POST':
		if partner:
			form1 = ProfileFormPartner(request.POST, request.FILES, instance=request.user)
		else:
			form1 = ProfileForm(request.POST, request.FILES, instance=request.user)

		if form1.is_valid():
			form1.save()
			messages.add_message(request, messages.INFO, 'Данные сохранены.')
			return HttpResponseRedirect('/accounts/profile/')
	else:
		if partner:
			form1 = ProfileFormPartner(instance=request.user, initial={'last_name':request.user.last_name, 'first_name':request.user.first_name, 'email':request.user.email})
		else:
			form1 = ProfileForm(instance=request.user, initial={'last_name':request.user.last_name, 'first_name':request.user.first_name, 'email':request.user.email})
		
	form2 = PasswordChangeForm(request.user)

	return render_to_response('profile.html', {'form1':form1, 'form2':form2, 'profile_nav':1}, RequestContext(request))
	
##########################################################################
##########################################################################

from forum.models import Forum, Thread, Post, Subscription

FORUM_PAGINATION = getattr(settings, 'FORUM_PAGINATION', 10)

#Темы в форуме созданные пользователем
@login_required
def profile_thread(request):
	t = Thread.objects.select_related().filter(author=request.user).order_by('id')
    
	return object_list( 
		request,
		queryset = t,
		paginate_by = FORUM_PAGINATION,
		template_object_name = 'thread',
		template_name = 'forum/profile_thread_list.html',
		extra_context = {
			'profile_nav': 2,
		}
	)
	
#Сообщения в форуме созданные пользователем
@login_required
def profile_post(request):
	p = Post.objects.select_related().filter(author=request.user).order_by('time')
    
	return object_list( 
		request,
		queryset = p,
		paginate_by = FORUM_PAGINATION,
		template_object_name = 'post',
		template_name = 'forum/profile_post_list.html',
		extra_context = {
			'profile_nav': 3,
		}
	)

##########################################################################
##########################################################################

from django.template import RequestContext
from registration.models import RegistrationProfile

def activate_partner(request, activation_key, template_name='registration/activate_partner.html', extra_context=None):

	activation_key = activation_key.lower() # Normalize before trying anything with it.
	account = RegistrationProfile.objects.activate_user(activation_key)
	if extra_context is None:
		extra_context = {}
	context = RequestContext(request)
	for key, value in extra_context.items():
		context[key] = callable(value) and value() or value
	if account:
		from threadmail import threading_send_mail
		current_site = Site.objects.get_current()
		subject = render_to_string('registration/activation_email_subject.txt', { 'site': current_site })
		threading_send_mail('registration/activation_partner_message.html', u'%s' % subject, [account.email,],{'account': account,	'site': current_site,})
	return render_to_response(template_name, { 'account': account, 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS }, context_instance=context)