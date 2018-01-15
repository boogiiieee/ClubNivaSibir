# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.html import escape

try:
    from markdown import markdown
except ImportError:
    class MarkdownNotFound(Exception):
        def __str__(self):
            return "Markdown is not installed!"
    raise MarkdownNotFound

##########################################################################
##########################################################################

def get_last_messages(self, user):
	return Message.objects.filter( (Q(from_user=self) & Q(for_user=user)) | (Q(from_user=user) & Q(for_user=self)) ).latest('created_at')

User.add_to_class("get_last_messages", get_last_messages)

def get_count_messages(self, from_user=None):
	tmp = Message.objects.filter(for_user=self, is_read=False)
	if from_user:
		tmp = tmp.filter(from_user=from_user)
	return tmp.count()
	
User.add_to_class("get_count_messages", get_count_messages)

#Сообщения пользователя
class Message(models.Model):
	from_user = models.ForeignKey(User, verbose_name=u'отправитель', related_name=u'from_users')
	for_user = models.ForeignKey(User, verbose_name=u'получатель', related_name=u'for_users')
	text = models.TextField(max_length=500, verbose_name=u'сообщение')
	text_html = models.TextField(editable=False, verbose_name=u'сообщение html')
	is_read = models.BooleanField(verbose_name=u'прочитано', default=False)
	created_at = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	
	def __unicode__(self):
		return u'%s -> %s' % (self.from_user.username, self.for_user.username)
		
	class Meta: 
		verbose_name = u'сообщение' 
		verbose_name_plural = u'сообщения пользователей'
		ordering = ['-id']
		
	def save(self, *args, **kwargs):
		self.text_html = markdown(escape(self.text))
		super(Message, self).save(*args, **kwargs)
		
##########################################################################
##########################################################################