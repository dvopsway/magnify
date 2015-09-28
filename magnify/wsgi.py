import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/mmt_bi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmt_bi.settings")
application = get_wsgi_application()