from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tasks.models import Board, Task


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name", "description"]
        labels = {
            "name": "Nombre",
            "description": "Descripción",
        }


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
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        task_list_queryset = self.fields["task_list"].queryset.select_related("board")
        tag_queryset = self.fields["tags"].queryset.select_related("board")

        if board is not None:
            task_list_queryset = task_list_queryset.filter(board=board)
            tag_queryset = tag_queryset.filter(board=board)
        elif user is not None and user.is_authenticated:
            task_list_queryset = task_list_queryset.filter(board__owner=user)
            tag_queryset = tag_queryset.filter(board__owner=user)
        else:
            task_list_queryset = task_list_queryset.none()
            tag_queryset = tag_queryset.none()

        self.fields["task_list"].queryset = task_list_queryset.order_by("board__name", "position", "name")
        self.fields["assignee"].queryset = self.fields["assignee"].queryset.order_by("username")
        self.fields["tags"].queryset = tag_queryset.order_by("board__name", "name")
