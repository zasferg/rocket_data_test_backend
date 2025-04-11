import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_app.settings')

app = Celery('test_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'increase_debt_every_3_hours': {
        'task': 'api.tasks.increase_debt',
        'schedule': crontab(minute=0, hour='*/3'),
    },
    'decrease_debt_every_day_6_30': {
        'task': 'api.tasks.decrease_debt',
        'schedule': crontab(minute=30),

    },
}


app.autodiscover_tasks()