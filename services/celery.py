import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')

app = Celery('services')

app.config_from_object("django.conf:settings", namespace='CELERY')

app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'elapsed-token-time': {
#         'task': 'account.tasks.delete_expired_tokens',
#         'schedule': crontab(minute='*/10')
#     }
# }