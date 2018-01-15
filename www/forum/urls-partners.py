"""
URLConf for Django-Forum.

django-forum assumes that the forum application is living under
/forum/.

Usage in your base urls.py:
    (r'^forum/', include('forum.urls')),

"""

from django.conf.urls.defaults import *
from forum.models import Forum
from forum.feeds import RssForumFeed, AtomForumFeed
from forum.sitemap import ForumSitemap, ThreadSitemap, PostSitemap

feed_dict = {
    'rss' : RssForumFeed,
    'atom': AtomForumFeed
}

sitemap_dict = {
    'forums': ForumSitemap,
    'threads': ThreadSitemap,
    'posts': PostSitemap,
}

urlpatterns = patterns('',
	url(r'^$', 'forum.views.forums_list', {'flag_partner': True,}, name='forum_index_partner'),

	url(r'^(?P<url>(rss|atom).*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feed_dict,}),

	url(r'^thread/(?P<thread>[0-9]+)/$', 'forum.views.thread', {'flag_partner': True,}, name='forum_view_thread_partner'),
	url(r'^post_edit/(?P<post>[0-9]+)/$', 'forum.views.post_edit', {'flag_partner': True,}, name='forum_view_post_edit_partner'),
	url(r'^thread/(?P<thread>[0-9]+)/reply/$', 'forum.views.reply', {'flag_partner': True,}, name='forum_reply_thread_partner'),

	url(r'^subscriptions/$', 'forum.views.updatesubs', {'flag_partner': True,}, name='forum_subscriptions_partner'),

	url(r'^(?P<slug>[-\w]+)/$', 'forum.views.forum', {'flag_partner': True,}, name='forum_thread_list_partner'),
	url(r'^(?P<forum>[-\w]+)/new/$', 'forum.views.newthread', {'flag_partner': True,}, name='forum_new_thread_partner'),

	url(r'^([-\w/]+/)(?P<forum>[-\w]+)/new/$', 'forum.views.newthread', {'flag_partner': True,}),
	url(r'^([-\w/]+/)(?P<slug>[-\w]+)/$', 'forum.views.forum', {'flag_partner': True,}, name='forum_subforum_thread_list_partner'),

	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemap_dict}),
	(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap_dict}),
)
