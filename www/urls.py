from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from django.contrib.sitemaps import FlatPageSitemap
from forum.sitemap import ForumSitemap, ThreadSitemap, PostSitemap
from news.views import NewsSitemap
from gallery.views import GallerySitemap

sitemaps = {
	'flatpages': FlatPageSitemap,
	'news':NewsSitemap,
	'gallery':GallerySitemap,
	
	'forum':ForumSitemap,
	'forum_thread':ThreadSitemap,
	'forum_post':PostSitemap,
}

urlpatterns = patterns('',
	url(r'^', include('project.urls')),
	url(r'^accounts/profile/messages/', include('user_msg.urls')),
	
	url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'registration/password_reset_form1.html', 'email_template_name':'registration/password_reset_email1.html'} ),
	url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'registration/password_reset_done1.html',} ),
	url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'registration/password_reset_confirm1.html',} ),
	url(r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'registration/password_reset_complete1.html',} ),
	url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='auth_logout'),
	url(r'^accounts/login/$', auth_views.login),
	url(r'^accounts/', include('registration.urls')),
	
	url(r'^admin/filebrowser/', include('filebrowser.urls')),
	url(r'^tinymce/', include('tinymce.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin_tools/', include('admin_tools.urls')),

	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^captcha/', include('captcha.urls')),
	
	url(r'^news/', include('news.urls')),
	url(r'^gallery/', include('gallery.urls')),
	
	url(r'^forum/', include('forum.urls')),
	url(r'^forum-partners/', include('forum.urls-partners')),
	# url(r'^like/', include('like.urls')),
	
	url(r'^comments/', include('django.contrib.comments.urls')),
	
	url(r'^configuration', include('configuration.urls')),
)

urlpatterns += patterns('',
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	url(r'^robots\.txt$', 'django.views.static.serve', {'path':"/robots.txt", 'document_root':settings.MEDIA_ROOT, 'show_indexes': False}),
)