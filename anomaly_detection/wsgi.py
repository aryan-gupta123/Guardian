"""
WSGI config for anomaly_detection project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anomaly_detection.settings')

application = get_wsgi_application()

