from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import override

from tasks.models import Board, Tag, Task, TaskList


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "No hemos podido iniciar sesión con esos datos. Revisa tu usuario y tu contraseña e inténtalo de nuevo.",
        "inactive": "Esta cuenta está desactivada en este momento.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["password"].label = "Contraseña"
        self.fields["username"].error_messages["required"] = "Escribe tu usuario para continuar."
        self.fields["password"].error_messages["required"] = "Escribe tu contraseña para continuar."


class RegisterForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        "password_mismatch": "Las contraseñas no coinciden. Revisa ambos campos y vuelve a intentarlo.",
    }

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["username"].help_text = "Hasta 50 caracteres. Puedes usar letras, números y @/./+/-/_."
        self.fields["password1"].help_text = (
            "<ul>"
            "<li>Tu contraseña no puede parecerse demasiado a tu información personal.</li>"
            "<li>Tu contraseña debe contener al menos 8 caracteres.</li>"
            "<li>Tu contraseña no puede ser una clave demasiado común.</li>"
            "<li>Tu contraseña no puede estar formada solo por números.</li>"
            "</ul>"
        )
        self.fields["password2"].help_text = "Repite la misma contraseña para confirmar que la has escrito bien."
        self.fields["username"].error_messages["required"] = "Escribe un nombre de usuario para crear tu cuenta."
        self.fields["username"].error_messages["max_length"] = "El nombre de usuario no puede superar los 150 caracteres."
        self.fields["password1"].error_messages["required"] = "Escribe una contraseña para continuar."
        self.fields["password2"].error_messages["required"] = "Confirma la contraseña para continuar."
        for validator in self.fields["username"].validators:
            if hasattr(validator, "message"):
                validator.message = "Introduce un nombre de usuario válido. Puedes usar letras, números y @/./+/-/_."

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and self._meta.model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese nombre de usuario. Prueba con otro.")
        return username

    def validate_password_for_user(self, user, password_field_name="password2"):
        with override("es"):
            super().validate_password_for_user(user, password_field_name=password_field_name)


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name", "description"]
        labels = {
            "name": "Nombre",
            "description": "Descripción",
        }


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ["name"]
        labels = {
            "name": "Nombre",
        }

    def __init__(self, *args, **kwargs):
        self.board = kwargs.pop("board", None)
        super().__init__(*args, **kwargs)
        if self.board is not None:
            self.instance.board = self.board

    def save(self, commit=True):
        task_list = super().save(commit=False)
        if self.board is not None:
            task_list.board = self.board
        if commit:
            task_list.save()
        return task_list

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name or self.board is None:
            return name

        duplicates = TaskList.objects.filter(board=self.board, name=name)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)

        if duplicates.exists():
            raise forms.ValidationError("Ya existe una lista con ese nombre en este tablero.")

        return name


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        labels = {
            "name": "Nombre",
        }

    def __init__(self, *args, **kwargs):
        self.board = kwargs.pop("board", None)
        super().__init__(*args, **kwargs)
        if self.board is not None:
            self.instance.board = self.board

    def save(self, commit=True):
        tag = super().save(commit=False)
        if self.board is not None:
            tag.board = self.board
        if commit:
            tag.save()
        return tag

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name or self.board is None:
            return name

        duplicates = Tag.objects.filter(board=self.board, name=name)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)

        if duplicates.exists():
            raise forms.ValidationError("Ya existe una etiqueta con ese nombre en este tablero.")

        return name


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha límite",
    )

    class Meta:
        model = Task
        fields = ["title", "description", "task_list", "assignee", "priority", "due_date", "tags"]
        labels = {
            "title": "Título",
            "description": "Descripción",
            "task_list": "Lista",
            "assignee": "Asignada a",
            "priority": "Prioridad",
            "tags": "Etiquetas",
        }
        widgets = {
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "task-form-tag-checkbox"}),
        }

    def __init__(self, *args, **kwargs):
        board = kwargs.pop("board", None)
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.board = board
        assignee_board = self._resolve_assignee_board(board=board, user=user)
        task_list_queryset = self.fields["task_list"].queryset.select_related("board")
        tag_queryset = self.fields["tags"].queryset.select_related("board")
        assignee_queryset = self.fields["assignee"].queryset

        if board is not None:
            task_list_queryset = task_list_queryset.filter(board=board)
            tag_queryset = tag_queryset.filter(board=board)
            assignee_queryset = assignee_queryset.filter(pk=board.owner_id)
        elif user is not None and user.is_authenticated:
            task_list_queryset = task_list_queryset.filter(board__owner=user)
            tag_queryset = tag_queryset.none()
            if assignee_board is not None:
                assignee_queryset = assignee_queryset.filter(pk=assignee_board.owner_id)
            else:
                assignee_queryset = assignee_queryset.filter(pk=user.pk)
        else:
            task_list_queryset = task_list_queryset.none()
            tag_queryset = tag_queryset.none()
            assignee_queryset = assignee_queryset.none()

        self.fields["task_list"].queryset = task_list_queryset.order_by("board__name", "position", "name")
        self.fields["assignee"].queryset = assignee_queryset.order_by("username")
        self.fields["assignee"].empty_label = "Sin asignar"
        if board is None:
            self.fields.pop("tags")
        else:
            self.fields["tags"].queryset = tag_queryset.order_by("board__name", "name")

    def _resolve_assignee_board(self, *, board, user):
        if board is not None:
            return board

        if self.instance.pk and self.instance.task_list_id:
            return self.instance.task_list.board

        if user is None or not user.is_authenticated:
            return None

        task_list_pk = self.data.get(self.add_prefix("task_list"))
        if task_list_pk is None:
            task_list_pk = self.initial.get("task_list")

        if task_list_pk in (None, ""):
            return None

        task_list = (
            TaskList.objects.filter(board__owner=user)
            .select_related("board")
            .filter(pk=task_list_pk)
            .first()
        )
        return task_list.board if task_list is not None else None


class TaskMoveForm(forms.Form):
    task_list = forms.ChoiceField(
        label="Mover a",
        choices=(),
        error_messages={
            "required": "Selecciona una lista válida.",
            "invalid_choice": "Selecciona una lista válida.",
        },
    )

    def __init__(self, *args, **kwargs):
        self.board = kwargs.pop("board")
        self.task = kwargs.pop("task")
        super().__init__(*args, **kwargs)
        self.available_task_lists = {
            str(task_list.pk): task_list
            for task_list in self.board.task_lists.all()
            if task_list.pk != self.task.task_list_id
        }
        self.fields["task_list"].choices = [
            (task_list_pk, task_list.name)
            for task_list_pk, task_list in self.available_task_lists.items()
        ]
        self.has_available_task_lists = bool(self.available_task_lists)

    def clean_task_list(self):
        task_list = self.available_task_lists.get(self.cleaned_data["task_list"])
        if task_list is None:
            raise forms.ValidationError("Selecciona una lista válida.")
        return task_list
