from django.urls import path

from tasks.views import task_create, task_list

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
]
