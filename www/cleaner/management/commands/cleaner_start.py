# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import settings
import datetime
import os, re

from cleaner.conf import settings as conf
	
#######################################################################################################################
#######################################################################################################################

class Command(NoArgsCommand):
	help = "Clean site"

	def handle_noargs(self, **options):
		from django.db import transaction
		from django.contrib.sessions.models import Session
		Session.objects.filter(expire_date__lt=datetime.datetime.now()).delete()
		transaction.commit_unless_managed()
		print 'Session cleaned.'
		
		try: from captcha.models import CaptchaStore
		except: pass
		else:
			CaptchaStore.remove_expired()
			print 'Captcha cleaned.'
		
		#Удаляем неиспользующиеся файлы из upload
		from django.db.models import get_app, get_models
		from django.db.models.fields import files

		#Перечисляем приложения
		for app in conf.APPS:
			app = get_app(app)
			
			#Перечисляем модели
			for model in get_models(app):
				#Перечисляем поля модели
				for field in model._meta.fields:
					if isinstance(field, files.FileField) or isinstance(field, files.ImageField):
						#Получаем пути файловых полей
						upload_to = os.path.realpath(os.path.join(settings.MEDIA_ROOT, field.upload_to))
						if os.path.exists(upload_to):
							#Перечисляем все файлы
							for filename in os.listdir(upload_to):
								fullname = os.path.join(upload_to, filename)
								if os.path.isfile(fullname):
									print '.', fullname
									value_filename = ''.join([settings.MEDIA_URL, field.upload_to, filename])
									#Проверяем используется ли файл в модели
									flag = False
									for row in model.objects.all():
										value = getattr(row, field.name, None)
										if value:
											value = unicode(value.url)

											pattern = re.compile(r'%s' % value, re.IGNORECASE)
											if pattern.search(value_filename):
												flag = True
									if not flag:
										os.remove(os.path.join(upload_to, filename))
										print 'DELETE'
		print 'Model files cleaned.'
		
		from django.core.cache import cache
		cache.clear() 
		print 'Cache cleaned.'
		
		try: from sorl.thumbnail import default
		except: pass
		else:
			try: default.kvstore.cleanup()
			except: print 'except in kvstore.cleanup'
			
			try: default.kvstore.clear()
			except: print 'except in kvstore.clear'
			
			try:
				cache_dir = os.path.realpath(os.path.join(settings.MEDIA_ROOT, 'cache'))
				for dirpath,dirnames,filenames in os.walk(cache_dir, topdown=False):
					for filename in filenames:
						os.remove(os.path.join(dirpath, filename))
					for filename in dirnames:
						os.rmdir(os.path.join(dirpath, filename))
			except: print 'except in remove files and dirs'
			print 'Sorl.thumbnail cleaned.'
		
		try: from watermark.models import Watermark
		except: pass
		else:
			for str in Watermark.objects.all():
				if str.image or str.wimage:
					im_path = os.path.realpath(os.path.join(os.path.dirname(settings.MEDIA_ROOT), '%s') % str.image)
					wm_path = os.path.realpath(os.path.join(os.path.dirname(settings.MEDIA_ROOT), '%s') % str.wimage)
					if not os.path.exists(wm_path) or not os.path.exists(im_path):
						str.delete()
						
			path = os.path.join(settings.MEDIA_ROOT, 'cache')
			for dirpath,dirnames,filenames in os.walk(path):
				for filename in filenames:
					r = re.compile('^([a-zA-Z0-9_-]+)_watermark\.([a-zA-Z0-9_-]+)$', re.IGNORECASE)
					if r.findall(filename):
						if not Watermark.objects.filter(wimage = os.path.join(dirpath, filename).replace(os.path.dirname(settings.MEDIA_ROOT), '')):
							os.remove(os.path.join(dirpath, filename))
			print 'Wotermark cleaned.'

#######################################################################################################################
#######################################################################################################################
