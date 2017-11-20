# quick_publisher/celery.py
 
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botsend.settings')
 
app = Celery('botsend')
app.config_from_object('django.conf:settings')
 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

'''app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'facebot.tasks.send_report',
        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` 
    },
}'''