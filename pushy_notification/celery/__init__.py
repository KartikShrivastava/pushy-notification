import os
import celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pushy_notification.settings')

celery_app = celery.Celery('pushy_notification')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
