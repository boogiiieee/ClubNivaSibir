# -*- coding: utf-8 -*-

from django.template import loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
import settings

from user_msg.models import Message
from user_msg.forms import MessageForm

PAGINATION = getattr(settings, 'USER_MSG_PAGINATION', 10)

##########################################################################
##########################################################################

#Написать сообщение
@login_required
def user_msg_careate(request):
	try:
		id = int( request.GET.get('u') )
	except:
		raise Http404()
		
	for_user = get_object_or_404(User, id=id)
		
	if request.method == 'POST':
		m = Message(from_user=request.user, for_user=for_user)
		form = MessageForm(request.POST, instance=m)
		if form.is_valid() and for_user != request.user:
			form.save()
			messages.add_message(request, messages.INFO, 'Сообщение отправлено.')
			return HttpResponseRedirect(
				reverse('user_msg.views.user_msg_messages', args=(), kwargs={'dialog_id':id})
			)
	else:
		form = MessageForm()
	return render_to_response('user_msg/create.html', {'profile_nav':4, 'for_user':for_user, 'form':form}, RequestContext(request))

##########################################################################
##########################################################################

#Список диалогов
@login_required
def user_msg_dialog(request):
	pks = []
	for i in Message.objects.filter( Q(from_user=request.user) | Q(for_user=request.user) ):
		pks.append(i.from_user.pk)
		pks.append(i.for_user.pk)
	pks = list(set(pks))
	
	queryset = User.objects.filter(pk__in=pks).exclude(pk=request.user.pk)
	
	return object_list(request,
		queryset = queryset,
		paginate_by = PAGINATION,
		template_object_name = 'dialog',
		template_name = 'user_msg/dialog.html',
		extra_context = {
			'profile_nav': 5,
		}
	)

##########################################################################
##########################################################################

#Исходящие сообщения
@login_required
def user_msg_messages(request, dialog_id):
	u = get_object_or_404(User, id=dialog_id)
	
	if request.method == 'POST':
		m = Message(from_user=request.user, for_user=u)
		form = MessageForm(request.POST, instance=m)
		if form.is_valid() and u != request.user:
			form.save()
			messages.add_message(request, messages.INFO, 'Сообщение отправлено.')
			return HttpResponseRedirect(
				reverse('user_msg.views.user_msg_messages', args=(), kwargs={'dialog_id':u.pk})
			)
	else:
		form = MessageForm()
	
	queryset = Message.objects.filter(
		(Q(from_user=u) & Q(for_user=request.user)) | (Q(from_user=request.user) & Q(for_user=u))
	).distinct()
	
	queryset.filter(for_user=request.user).update(is_read=True)
	
	return object_list(request,
		queryset = queryset,
		paginate_by = PAGINATION,
		template_object_name = 'messages',
		template_name = 'user_msg/messages.html',
		extra_context = {
			'profile_nav': 5,
			'form': form,
			'u': u,
		}
	)

##########################################################################
##########################################################################