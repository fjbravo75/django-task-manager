from django.urls import path

from tasks.views import task_create, task_detail, task_list

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('create/', task_create, name='task_create'),
]
