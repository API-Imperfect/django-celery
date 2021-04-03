from __future__ import absolute_import

import os
import time

from django.conf import settings

from celery import Celery

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_celery_example.settings")

# you change the name here
app = Celery("django_celery_example")

# read config from Django settings, the CELERY namespace would make celery
# config keys have 'CELERY' prefix
# tells Celery to read values from the CELERY namespace in settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def add(x, y):
    # from celery.contrib import rdb

    # rdb.set_trace()

    time.sleep(10)
    return x / y
