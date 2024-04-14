"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config

config_mode = config("CONFIG_MODE")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{config_mode}")

application = get_wsgi_application()
