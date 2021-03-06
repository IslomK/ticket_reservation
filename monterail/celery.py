from __future__ import absolute_import, unicode_literals
import os

import django
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monterail.settings')
django.setup()

app = Celery('monterail', include='api.tasks')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.task_default_queue = 'monterail_queue'
app.conf.beat_schedule = {
    "update_reservation_status": {
        "task": "api.tasks.update_reservation_status",
        "schedule": crontab(hour='*/15')
    }
}

