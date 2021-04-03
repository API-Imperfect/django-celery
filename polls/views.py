import json
import random

import requests
from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render

from polls.forms import YourForm
from polls.tasks import sample_task


# helpers
def api_call(email):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception("random processing error")

    # used for simulating a call to a third party api
    requests.post("https://httpbin.org/delay/5")


# views


def form(request):
    if request.is_ajax() and request.method == "POST":
        form = YourForm(request.POST)
        if form.is_valid():
            task = sample_task.delay(form.cleaned_data["email"])
            # return the task id so the JS can poll the state
            return JsonResponse(
                {
                    "task_id": task.task_id,
                }
            )
    form = YourForm()
    return render(request, "form.html", {"form": form})


def task_status(request):
    task_id = request.GET.get("task_id")

    if task_id:
        task = AsyncResult(task_id)
        if task.state == "FAILURE":
            error = str(task.result)
            response = {
                "state": task.state,
                "error": error,
            }
        else:
            response = {"state": task.state}
        return JsonResponse(response)
