# -*- coding: utf-8 -*-

"""
All forum logic is kept here - displaying lists of forums, threads 
and posts, adding new threads, and adding replies.
"""

from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.template import RequestContext, Context, loader
from django import forms
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.defaultfilters import striptags, wordwrap
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.contrib import messages
from django.shortcuts import redirect

from forum.models import Forum, Thread, Post, AttachFile, Subscription
from forum.forms import CreateThreadForm, ReplyForm, AttachFileFormset, PostEditForm

FORUM_PAGINATION = getattr(settings, 'FORUM_PAGINATION', 10)
LOGIN_URL = getattr(settings, 'LOGIN_URL', '/accounts/login/')

def forums_list(request, flag_partner=False):
	if flag_partner:
		if request.user.is_authenticated() and request.user.get_profile().is_partner():
			queryset = Forum.objects.for_groups(request.user.groups.all()).filter(parent__isnull=True, for_partner=flag_partner)
		else:
			messages.add_message(request, messages.ERROR, 'Пожалуйста, авторизируйтесь как партнер.')
			return redirect('/accounts/login/?next=%s' % request.path)
	else:queryset = Forum.objects.for_groups(request.user.groups.all()).filter(parent__isnull=True, for_partner=flag_partner)
	return object_list(request, queryset=queryset, extra_context = {'flag_partner':flag_partner})

def forum(request, slug, flag_partner=False):
	"""
	Displays a list of threads within a forum.
	Threads are sorted by their sticky flag, followed by their 
	most recent post.
	"""
	try:
		if flag_partner:
			if request.user.is_authenticated() and request.user.get_profile().is_partner():
				f = Forum.objects.for_groups(request.user.groups.all()).select_related().get(slug=slug, for_partner=flag_partner)
			else:
				messages.add_message(request, messages.ERROR, 'Пожалуйста, авторизируйтесь как партнер.')
				return redirect('/accounts/login/?next=%s' % request.path)
		else: 
			f = Forum.objects.for_groups(request.user.groups.all()).select_related().get(slug=slug, for_partner=flag_partner)
	except Forum.DoesNotExist:
		raise Http404

	form = CreateThreadForm()
	formset = AttachFileFormset()
	
	child_forums = f.child.for_groups(request.user.groups.all())
	
	return object_list(
		request,
		queryset=f.thread_set.select_related().all(),
		paginate_by=FORUM_PAGINATION,
		template_object_name='thread',
		template_name='forum/thread_list.html',
		extra_context = {
			'forum': f,
			'formset': formset,
			'child_forums': child_forums,
			'form': form,
			'flag_partner':flag_partner
		}
	)

def thread(request, thread, flag_partner=False):
	"""
	Increments the viewed count on a thread then displays the 
	posts for that thread, in chronological order.
	"""
	try:
		t = Thread.objects.select_related().get(pk=thread, forum__for_partner=flag_partner)
		if t.forum.for_partner:
			if request.user.is_authenticated() and request.user.get_profile().is_partner():pass
			else:
				messages.add_message(request, messages.ERROR, 'Пожалуйста, авторизируйтесь как партнер.')
				return redirect('/accounts/login/?next=%s' % request.path)
		if not Forum.objects.has_access(t.forum, request.user.groups.all()):
			raise Http404
	except Thread.DoesNotExist: raise Http404

	
	p = t.post_set.select_related('author').all().order_by('time')
	s = None
	if request.user.is_authenticated():
		s = t.subscription_set.select_related().filter(author=request.user)

	t.views += 1
	t.save()

	if s: initial = {'subscribe': True}
	else: initial = {'subscribe': False}

	form = ReplyForm(initial=initial)
	formset = AttachFileFormset()

	return object_list(
		request,
		queryset=p,
		paginate_by=FORUM_PAGINATION,
		template_object_name='post',
		template_name='forum/thread.html',
		extra_context = {
			'forum': t.forum,
			'thread': t,
			'subscription': s,
			'form': form,
			'formset': formset,
			'flag_partner':flag_partner
		}
	)
	
def post_edit(request, post, flag_partner=False):
	if flag_partner:
		if request.user.is_authenticated() and request.user.get_profile().is_partner():pass
		else:
			messages.add_message(request, messages.ERROR, 'Пожалуйста, авторизируйтесь как партнер.')
			return redirect('/accounts/login/?next=%s' % request.path)
	try:
		t = Post.objects.get(pk=post, thread__forum__for_partner=flag_partner)
	except Post.DoesNotExist: raise Http404
	if t.author == request.user:
		form = PostEditForm(initial = {'body' : t.body})
		if request.method == "POST":
			form = PostEditForm(request.POST)
			if form.is_valid():
				t.body = form.cleaned_data['body']
				t.save()
				return HttpResponseRedirect(t.get_absolute_url())

		return render_to_response('forum/edit_post.html',
			RequestContext(request, {
				'post': t,
				'form': form,
				'forum': t.thread.forum,
				'thread': t.thread,
				'flag_partner':flag_partner
			}
		))
	else:
		return HttpResponseRedirect(t.get_absolute_url())

def reply(request, thread, flag_partner=False):
	"""
	If a thread isn't closed, and the user is logged in, post a reply
	to a thread. Note we don't have "nested" replies at this stage.
	"""
	if flag_partner:
		if request.user.is_authenticated() and request.user.get_profile().is_partner():pass
		else:
			messages.add_message(request, messages.ERROR, 'Пожалуйста, авторизируйтесь как партнер.')
			return redirect('/accounts/login/?next=%s' % request.path)
			
	if not request.user.is_authenticated():
		return HttpResponseRedirect('%s?next=%s' % (LOGIN_URL, request.path))
	t = get_object_or_404(Thread, pk=thread)
	if t.closed:
		return HttpResponseServerError()
	if not Forum.objects.has_access(t.forum, request.user.groups.all()):
		return HttpResponseForbidden()

	if request.method == "POST":
		form = ReplyForm(request.POST)
		formset = AttachFileFormset(request.POST, request.FILES)
		if form.is_valid() and formset.is_valid():
			p = Post(
				thread=t,
				author=request.user,
				body=form.cleaned_data['body'],
				time=datetime.now(),
			)
			p.save()
			
			formset.instance = p
			formset.save()

			sub = Subscription.objects.filter(thread=t, author=request.user)
			if form.cleaned_data.get('subscribe',False):
				if not sub:
					s = Subscription(author=request.user, thread=t)
					s.save()
			else:
				if sub: sub.delete()

			if t.subscription_set.count() > 0:
				mail_subject = ''
				try: mail_subject = settings.FORUM_MAIL_PREFIX 
				except AttributeError: mail_subject = '[Forum]'

				mail_from = ''
				try: mail_from = settings.FORUM_MAIL_FROM
				except AttributeError: mail_from = settings.DEFAULT_FROM_EMAIL

				mail_tpl = loader.get_template('forum/notify.txt')
				body = form.cleaned_data['body']
				c = Context({
					'body': wordwrap(striptags(body), 72),
					'site' : Site.objects.get_current(),
					'thread': t,
				})

				email = EmailMessage(
					subject=mail_subject+' '+striptags(t.title),
					body= mail_tpl.render(c),
					from_email=mail_from,
					bcc=[s.author.email for s in t.subscription_set.all()],)
				email.send(fail_silently=True)

			return HttpResponseRedirect(p.get_absolute_url())
	else:
		form = ReplyForm()
		formset = AttachFileFormset()
    
	return render_to_response('forum/reply.html',
		RequestContext(request, {
			'form': form,
			'formset': formset,
			'forum': t.forum,
			'thread': t,
			'flag_partner':flag_partner
		}))


def newthread(request, forum, flag_partner=False):
	"""
	Rudimentary post function - this should probably use 
	newforms, although not sure how that goes when we're updating 
	two models.

	Only allows a user to post if they're logged in.
	"""
	if flag_partner:
		if request.user.is_authenticated() and request.user.get_profile().is_partner():pass
		else:
			messages.add_message(request, messages.ERROR, 'Пожалуйста, авторизируйтесь как партнер.')
			return redirect('/accounts/login/?next=%s' % request.path)
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('%s?next=%s' % (LOGIN_URL, request.path))

	f = get_object_or_404(Forum, slug=forum)
    
	if not Forum.objects.has_access(f, request.user.groups.all()):
		return HttpResponseForbidden()

	if request.method == 'POST':
		form = CreateThreadForm(request.POST)
		formset = AttachFileFormset(request.POST, request.FILES)
		if form.is_valid() and formset.is_valid():
			t = Thread(
				forum=f,
				author=request.user,
				title=form.cleaned_data['title'],
			)
			t.save()

			p = Post(
				thread=t,
				author=request.user,
				body=form.cleaned_data['body'],
				time=datetime.now(),
			)
			p.save()
			
			formset.instance = p
			formset.save()
    
			if form.cleaned_data.get('subscribe', False):
				s = Subscription(
					author=request.user,
					thread=t
				)
				s.save()
			return HttpResponseRedirect(t.get_absolute_url())
	else:
		form = CreateThreadForm()
		formset = AttachFileFormset()

	return render_to_response('forum/newthread.html',
		RequestContext(request, {
			'form': form,
			'formset': formset,
			'forum': f,
			'flag_partner':flag_partner
		}))

def updatesubs(request, flag_partner=False):
	"""
		Allow users to update their subscriptions all in one shot.
	"""
	if not request.user.is_authenticated():
		return HttpResponseRedirect('%s?next=%s' % (LOGIN_URL, request.path))

	subs = Subscription.objects.select_related().filter(author=request.user, thread__forum__for_partner=flag_partner)

	if request.POST:
		# remove the subscriptions that haven't been checked.
		post_keys = [k for k in request.POST.keys()]
		for s in subs:
			if not str(s.thread.id) in post_keys:
				s.delete()
		messages.add_message(request, messages.INFO, 'Данные сохранены.')
		return HttpResponseRedirect(reverse('forum_subscriptions'))

	return render_to_response('forum/updatesubs.html', RequestContext(request, {'subs': subs, 'next': request.GET.get('next'), 'flag_partner':flag_partner}))