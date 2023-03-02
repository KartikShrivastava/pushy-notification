import os
import celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pushy_notification.settings')

celery_app = celery.Celery('pushy_notification')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
