# -*- coding: utf-8 -*-

import os
from django.conf import settings

APPS = getattr(settings, 'CLEANER_APPS', ())