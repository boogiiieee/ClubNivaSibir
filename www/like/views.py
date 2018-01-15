# -*- coding: utf-8 -*-

from django.template import loader, RequestContext
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import datetime

try:
	import json
except:
	import simplejson as json

from like.models import Like, DoubleProtection

IP_CLICK_LIMIT = getattr(settings, 'LIKE_IP_CLICK_LIMIT', 10)
		
##########################################################################
##########################################################################

def add_like(request):
	if request.is_ajax():
		try:
			id = int( request.GET.get('id', 0) )
			name = str(request.GET.get('name', ''))
		except:
			pass
		else:
			if id and name:
				try:
					obj = Like.objects.get(id=id)
				except:
					data = {'result':-1}
				else:
					ip = request.META['REMOTE_ADDR']
					if ip:
						dp, create = DoubleProtection.objects.get_or_create(ip=ip, created=datetime.datetime.now())
						
						if dp.count > IP_CLICK_LIMIT:
							data = {'result':2}
						else:
							dp.count += 1
							dp.save()
							
							ctype, object_pk = ContentType.objects.get_for_model(obj), obj.id
							cookies_name = 'like_%s_%s_%s' % (ctype, object_pk, name)
							
							if cookies_name in request.session:
								data = {'result':2}
							else:
								request.session[cookies_name] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

								obj.like_count += 1
								obj.save()
								
								data = {'result':1, 'count':obj.like_count}
					else:
						data = {'result':-1}
						
				data = json.dumps(data)
				return HttpResponse(data)
			
	return HttpResponse(status=400)
	
##########################################################################
##########################################################################