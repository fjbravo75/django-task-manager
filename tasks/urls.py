from django.urls import path

from tasks.views import board_create, board_detail, board_list, board_task_list_create, task_create, task_delete, task_detail, task_list, task_update

urlpatterns = [
    path("", board_list, name="board_list"),
    path("boards/create/", board_create, name="board_create"),
    path("boards/<int:pk>/", board_detail, name="board_detail"),
    path("boards/<int:board_pk>/lists/create/", board_task_list_create, name="board_task_list_create"),
    path("boards/<int:board_pk>/tasks/create/", task_create, name="board_task_create"),
    path("tasks/", task_list, name="task_list"),
    path("tasks/create/", task_create, name="task_create"),
    path("tasks/<int:pk>/", task_detail, name="task_detail"),
    path("tasks/<int:pk>/edit/", task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", task_delete, name="task_delete"),
]
