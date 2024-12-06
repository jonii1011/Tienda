import os
import sys
from django.core.wsgi import get_wsgi_application

# Añadir el directorio de la aplicación a PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


