import json

from celery import shared_task


@shared_task()
def sample_task(email):
    from polls.views import api_call

    api_call(email)
