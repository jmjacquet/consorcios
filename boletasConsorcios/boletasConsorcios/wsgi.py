import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

sys.path.append(PROJECT_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'boletasConsorcios.settings'
os.environ['MUNI_ID'] = '220'
os.environ['MUNI_DB'] = 'grupogua_aires'
os.environ['MUNI_DIR'] = 'aires'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()