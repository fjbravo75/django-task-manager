from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha límite",
    )

    class Meta:
        model = Task
        fields = ["title", "description", "task_list", "priority", "assignee", "due_date", "tags"]
        labels = {
            "title": "Título",
            "description": "Descripción",
            "task_list": "Lista",
            "priority": "Prioridad",
            "assignee": "Asignado a",
            "tags": "Etiquetas",
        }

    def __init__(self, *args, **kwargs):
        board = kwargs.pop("board", None)
        super().__init__(*args, **kwargs)
        task_list_queryset = self.fields["task_list"].queryset.select_related("board")
        tag_queryset = self.fields["tags"].queryset.select_related("board")

        if board is not None:
            task_list_queryset = task_list_queryset.filter(board=board)
            tag_queryset = tag_queryset.filter(board=board)

        self.fields["task_list"].queryset = task_list_queryset.order_by("board__name", "position", "name")
        self.fields["assignee"].queryset = self.fields["assignee"].queryset.order_by("username")
        self.fields["tags"].queryset = tag_queryset.order_by("board__name", "name")
