# -*- coding: utf-8 -*-

from django.template import loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import list_detail, simple
from django.contrib.sitemaps import Sitemap

from gallery.conf import settings as conf
from gallery.models import CategoryGallery, PhotoGallery

##########################################################################
##########################################################################

#Для карты сайта
class GallerySitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.5
	
	def items(self):
		return CategoryGallery.activs.all()
		
	def location(self, obj):
		return obj.get_item_url()
		
##########################################################################
##########################################################################

def all(request, template_name='gallery/gallery.html', extra_context=None, context_processors=None, template_loader=loader):
	page = 1
	if 'page' in request.GET and request.GET.get('page'):
		try: page = int(request.GET.get('page'))
		except ValueError: raise Http404()
		
	objs = CategoryGallery.activs.all()
	
	return list_detail.object_list(
		request,
		queryset = objs,
		paginate_by = conf.PAGINATE_BY,
		page = page,
		template_name = template_name,
		template_object_name = 'items',
		extra_context = extra_context,
		context_processors = context_processors,
		template_loader = template_loader,
	)
	
##########################################################################
##########################################################################
	
def full(request, id, template_name='gallery/item.html', extra_context=None, context_processors=None, template_loader=loader):
	page = 1
	if 'page' in request.GET and request.GET.get('page'):
		try: page = int(request.GET.get('page'))
		except ValueError: raise Http404()
		
	try: id = int(id)
	except ValueError: raise Http404()
	
	try: cat = CategoryGallery.activs.get(id = id)
	except ValueError: raise Http404()
	
	objs = PhotoGallery.activs.filter(category = cat)
	
	return list_detail.object_list(
		request,
		queryset = objs,
		paginate_by = conf.PAGINATE_FOTO_BY,
		page = page,
		template_name = template_name,
		template_object_name = 'item',
		extra_context = {'cat':cat},
		context_processors = context_processors,
		template_loader = template_loader,
	)

	
##########################################################################
##########################################################################