import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

app = Celery('bookstore')

app.config_from_object('django.conf:settings', namespace='CELERY')
#app.config_from_object(settings.CELERY)

app.conf.broker_connection_always_reconnect = True
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

app.conf.beat_schedule = {}
