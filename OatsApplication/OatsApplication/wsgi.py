"""
WSGI config for OatsApplication project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "OatsApplication"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OatsApplication.settings')

application = get_wsgi_application()
