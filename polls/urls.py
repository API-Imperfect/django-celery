from django.urls import path

from polls.views import form, task_status

urlpatterns = [
    path("form/", form, name="form"),
    path("task_status/", task_status, name="task_status"),
]
