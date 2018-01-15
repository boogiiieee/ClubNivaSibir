# -*- coding: utf-8 -*-

import os
from django.conf import settings

PAGINATE_BY = getattr(settings, 'GALLERY_PAGINATE_BY', 2)
PAGINATE_FOTO_BY = getattr(settings, 'GALLERY_PAGINATE_FOTO_BY', 16)