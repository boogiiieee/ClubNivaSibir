# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'www.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'www.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.menu import items, Menu

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

class CustomMenuDashboard(Menu):
	def init_with_context(self, context):
		site_name = get_admin_site_name(context)

		self.children += [
			items.MenuItem(_('Dashboard'), reverse('%s:index' % site_name)),
			
			items.AppList(
				_('Applications'),
				exclude=(
					'django.contrib.*',
				)
			),
			
			items.MenuItem(_('Administration'),
				children=[
					items.MenuItem(_('Groups'), '/admin/auth/group/', enabled=context['request'].user.has_perm("auth.change_group")),
					items.MenuItem(_('Users'), '/admin/auth/user/', enabled=context['request'].user.has_perm("auth.change_user")),
					items.MenuItem(_('Sites'), '/admin/sites/site/', enabled=context['request'].user.has_perm("sites.change_site")),
				],
			),
			
			items.Bookmarks(),
			
			items.MenuItem(_('Google analytics'), 'http://www.google.com/intl/ru/analytics/'),
			items.MenuItem(_('Helpdesk'), 'http://web-aspect.ru/helpdesk/'),
		]

class CustomIndexDashboard(Dashboard):
	"""
	Custom index dashboard for www.
	"""
	def init_with_context(self, context):
		site_name = get_admin_site_name(context)
		
		self.children.append(modules.Group(
			title=_('Site'),
			display="tabs",
			children=[
				modules.LinkList(
					title=_('Index'),
					children=[
						[_('Flatpage'), '/admin/my_flatpages/flatpage/1/'],
						[_('Banners'), '/admin/banners/banner/'],
						[_('News'), '/admin/news/newsarticle/'],
					]
				),
				modules.LinkList(
					title=_('News'),
					children=[
						[_('Flatpage'), '/admin/my_flatpages/flatpage/5/'],
						[_('News'), '/admin/news/newsarticle/'],
					]
				),
				modules.LinkList(
					title=_('History'),
					children=[
						[_('Flatpage'), '/admin/my_flatpages/flatpage/2/'],
					]
				),
				modules.LinkList(
					title=_('Gallery'),
					children=[
						[_('Flatpage'), '/admin/my_flatpages/flatpage/3/'],
						[_('Gallery'), '/admin/gallery/categorygallery/'],
					]
				),
				modules.LinkList(
					title=_('Forum'),
					children=[
						[_('Flatpage'), '/admin/my_flatpages/flatpage/8/'],
						[_('Forum'), '/admin/forum/'],
					]
				),
				modules.LinkList(
					title=u'Партнеры',
					children=[
						[u'Текст', '/admin/my_flatpages/flatpage/16/'],
						[u'Список партнеров', '/admin/partners/partner/'],
					]
				),
				modules.LinkList(
					title=_('Contacts'),
					children=[
						[_('Flatpage'), '/admin/my_flatpages/flatpage/4/'],
						[_('Map'), '/admin/yandex_map/map/'],
						[_('Userphoto'), '/admin/userphoto/userphoto/'],
					]
				),
            ]
		))

		# append an app list module for "Administration"
		self.children.append(modules.AppList(
			_('Administration'),
			models=('django.contrib.*',),
		))
		
		# append a link list module for "filebrowser"
		self.children.append(modules.LinkList(
			_('FileBrowser'),
			children=[
				[_('FileBrowser'), '/admin/filebrowser/browse/'],
			]
		))
		
		# append a link list module for "quick links"
		self.children.append(modules.LinkList(
			_('Quick links'),
			layout='inline',
			draggable=False,
			deletable=False,
			collapsible=False,
			children=[
				[_('Return to site'), '/'],
				[_('Change password'),
				reverse('%s:password_change' % site_name)],
				[_('Log out'), reverse('%s:logout' % site_name)],
			]
		))
		
		from configuration.views import ConfigModule
		self.children.append(ConfigModule())

		# append a recent actions module
		self.children.append(modules.RecentActions(_('Recent Actions'), 5))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for www.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(_(self.app_title), self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
