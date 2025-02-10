import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.config.settings')

celery_app = Celery("django_app")

celery_app.config_from_object(f'django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
