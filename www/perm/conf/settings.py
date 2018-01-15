# -*- coding: utf-8 -*-

import os
from django.conf import settings

APPS = getattr(settings, 'APPS_PERM', {
	'auth': ['user', 'group'],
	'sites': ['site'],
})