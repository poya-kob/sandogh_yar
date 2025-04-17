from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sandogh_yar.settings')

app = Celery('sandogh_yar')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Optional: naming queues per app
app.conf.task_queues = {
    'default': {'exchange': 'default'},
    'loans': {'exchange': 'loans'},
    'reminders': {'exchange': 'reminders'},
}
