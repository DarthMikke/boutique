"""
ASGI config for boutique project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import dotenv

from django.core.asgi import get_asgi_application

env_file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'
)
print(f"Loading .env file from {env_file_path}")
dotenv.read_dotenv(env_file_path)
print(repr(os.environ))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique.settings')

application = get_asgi_application()
