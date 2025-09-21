"""
WSGI config for dcrm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcrm.settings")

# Determine the environment and load appropriate settings

# ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

# if ENVIRONMENT == 'production':

#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings.production')

# else:

#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings.development')


application = get_wsgi_application()
