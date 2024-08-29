"""
WSGI config for boutique project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

env_file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'
)
dotenv.read_dotenv(env_file_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique.settings')

application = get_wsgi_application()
