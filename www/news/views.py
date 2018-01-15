# -*- coding: utf-8 -*-

from django.template import loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import list_detail, simple
from django.contrib.sitemaps import Sitemap

from news.conf import settings as conf
from news.models import NewsArticle

##########################################################################
##########################################################################

#Для карты сайта
class NewsSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.5
	
	def items(self):
		return NewsArticle.activs.all()
		
	def location(self, obj):
		return obj.get_item_url()
		
##########################################################################
##########################################################################

def all(request, template_name='news/news.html', extra_context=None, context_processors=None, template_loader=loader):
	page = 1
	if 'page' in request.GET and request.GET.get('page'):
		try: page = int(request.GET.get('page'))
		except ValueError: raise Http404()
		
	objs = NewsArticle.activs.all()
	
	return list_detail.object_list(
		request,
		queryset = objs,
		paginate_by = conf.PAGINATE_BY,
		page = page,
		template_name = template_name,
		template_object_name = 'news',
		extra_context = extra_context,
		context_processors = context_processors,
		template_loader = template_loader,
	)
	
##########################################################################
##########################################################################
	
def full(request, id, template_name='news/item.html', extra_context=None, context_processors=None, template_loader=loader):
	try: id = int(id)
	except ValueError: raise Http404()
		
	objs = NewsArticle.activs.all()
	
	return list_detail.object_detail(
		request,
		queryset = objs,
		object_id = id,
		template_name = template_name,
		extra_context = extra_context,
		template_object_name='item',
		context_processors = context_processors,
		template_loader = template_loader,
	)
	
##########################################################################
##########################################################################