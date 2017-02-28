from __future__ import absolute_import

import os

from celery import Celery
from hirefire.procs.celery import CeleryProc

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarttools.settings')

from django.conf import settings

app = Celery('smarttools')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL = 'amqp://' + os.environ.get('RABBITMQ_HOST', '')
)

class WorkerProc(CeleryProc):
    # the name field should be identical with the worker name on your
    # Procfile!! It is nowhere explicitly written,
    # but otherwise it won't work!
    name = 'worker'
    queues = ['celery']
    app = app