from django.db import models


class Task(models.Model):
    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_DONE, "Done"),
    ]

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
