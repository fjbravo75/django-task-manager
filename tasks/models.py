from django.conf import settings
from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="boards",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self):
        return self.name


class TaskList(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="task_lists")
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["board_id", "position", "pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"],
                name="unique_task_list_name_per_board",
            ),
        ]

    def __str__(self):
        return f"{self.board.name} - {self.name}"


class Tag(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["board_id", "name", "pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"],
                name="unique_tag_name_per_board",
            ),
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Baja"),
        (PRIORITY_MEDIUM, "Media"),
        (PRIORITY_HIGH, "Alta"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.title

    def get_status_display(self):
        return self.task_list.name
