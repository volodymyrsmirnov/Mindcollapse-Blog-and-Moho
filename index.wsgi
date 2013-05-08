#!/usr/local/bin/python2.7
import sys
sys.path.append('/home/smirnov/www/mindcollapse.com')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
