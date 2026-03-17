from django.urls import path

from tasks.views import task_create, task_delete, task_detail, task_list, task_update

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('<int:pk>/edit/', task_update, name='task_update'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
    path('create/', task_create, name='task_create'),
]
