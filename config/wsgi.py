"""
WSGI config for Nexus Headless CMS.
Exposes the WSGI callable as `application` and `app` for Vercel Serverless Functions.
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Vercel serverless functions look for 'app'
app = application
