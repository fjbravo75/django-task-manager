from django.contrib import admin

from .models import Board, Tag, Task, TaskList


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at", "updated_at")
    search_fields = ("name", "description", "owner__username")
    filter_horizontal = ("members",)


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ("name", "board", "position")
    list_filter = ("board",)
    search_fields = ("name", "board__name")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "board")
    list_filter = ("board",)
    search_fields = ("name", "board__name")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_list", "priority", "assignee", "due_date", "updated_at")
    list_filter = ("priority", "task_list", "due_date")
    search_fields = ("title", "description", "task_list__name", "tags__name")
    filter_horizontal = ("tags",)
