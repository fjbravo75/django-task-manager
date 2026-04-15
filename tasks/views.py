import csv
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Max, Prefetch
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from tasks.demo_data import DEMO_USERNAME
from tasks.forms import BoardForm, LoginForm, RegisterForm, TagForm, TaskFilterForm, TaskForm, TaskListForm, TaskMoveForm
from tasks.models import Board, Tag, Task, TaskList

SPANISH_MONTH_ABBREVIATIONS = {
    1: "ene",
    2: "feb",
    3: "mar",
    4: "abr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dic",
}


class TaskLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "show_demo_access": True,
                "demo_username": DEMO_USERNAME,
                "demo_password": settings.DEMO_USER_PASSWORD,
            }
        )
        return context


def register(request):
    if request.user.is_authenticated:
        return redirect("board_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("board_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def board_list(request):
    boards = (
        Board.objects.filter(owner=request.user)
        .select_related("owner")
        .prefetch_related(
            Prefetch(
                "task_lists",
                queryset=TaskList.objects.order_by("position", "pk"),
            )
        )
        .order_by("name", "pk")
    )
    return render(request, "tasks/board_list.html", {"boards": boards})


@login_required
def board_create(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect("board_detail", pk=board.pk)
    else:
        form = BoardForm()

    context = {
        "form": form,
        "page_title": "Nuevo tablero",
        "screen_title": "Nuevo tablero",
        "screen_subtitle": "Crea un tablero para empezar a organizar tu trabajo.",
        "panel_title": "Detalles del tablero",
        "panel_subtitle": "Define el nombre y una breve descripción inicial del tablero.",
        "submit_label": "Guardar tablero",
        "cancel_url": "board_list",
        "cancel_url_kwargs": None,
        "back_label": "Volver a tableros",
    }
    return render(request, "tasks/board_form.html", context)


@login_required
def board_update(request, pk):
    board = get_object_or_404(
        Board.objects.filter(owner=request.user).select_related("owner"),
        pk=pk,
    )

    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect("board_detail", pk=board.pk)
    else:
        form = BoardForm(instance=board)

    context = {
        "form": form,
        "board": board,
        "page_title": f"Editar {board.name}",
        "screen_title": "Editar tablero",
        "screen_subtitle": "Actualiza los datos básicos de este tablero.",
        "panel_title": "Detalles del tablero",
        "panel_subtitle": "Solo puedes cambiar el nombre y la descripción de este tablero.",
        "submit_label": "Guardar cambios",
        "cancel_url": "board_detail",
        "cancel_url_kwargs": {"pk": board.pk},
        "back_label": "Volver al tablero",
    }
    return render(request, "tasks/board_form.html", context)


@login_required
def board_delete(request, pk):
    board = get_object_or_404(
        Board.objects.filter(owner=request.user).select_related("owner"),
        pk=pk,
    )

    if request.method == "POST":
        board.delete()
        return redirect("board_list")

    context = {
        "board": board,
        "task_list_count": board.task_lists.count(),
        "task_count": Task.objects.filter(task_list__board=board).count(),
        "page_title": f"Eliminar {board.name}",
        "screen_title": "Eliminar tablero",
        "screen_subtitle": "Confirma si quieres borrar este tablero de forma definitiva.",
        "panel_title": "Confirmación de borrado",
        "panel_subtitle": "Si confirmas, este tablero y todas sus listas y tareas asociadas se eliminarán para siempre.",
    }
    return render(request, "tasks/board_confirm_delete.html", context)


@login_required
def board_task_list_create(request, board_pk):
    board = get_object_or_404(
        Board.objects.filter(owner=request.user).select_related("owner"),
        pk=board_pk,
    )

    if request.method == "POST":
        form = TaskListForm(request.POST, board=board)
        if form.is_valid():
            task_list = form.save(commit=False)
            max_position = board.task_lists.aggregate(max_position=Max("position"))["max_position"] or 0
            task_list.board = board
            task_list.position = max_position + 1
            task_list.save()
            return redirect("board_detail", pk=board.pk)
    else:
        form = TaskListForm(board=board)

    context = {
        "form": form,
        "board": board,
        "page_title": "Nueva lista",
        "screen_title": "Nueva lista",
        "screen_subtitle": "Crea una nueva lista dentro del tablero actual.",
        "panel_title": "Detalles de la lista",
        "panel_subtitle": "Define el nombre de la lista que quieres añadir a este tablero.",
        "submit_label": "Guardar lista",
    }
    return render(request, "tasks/task_list_form.html", context)


@login_required
def board_tag_create(request, board_pk):
    board = get_object_or_404(
        Board.objects.filter(owner=request.user).select_related("owner"),
        pk=board_pk,
    )

    if request.method == "POST":
        form = TagForm(request.POST, board=board)
        if form.is_valid():
            form.save()
            return redirect("board_detail", pk=board.pk)
    else:
        form = TagForm(board=board)

    context = {
        "form": form,
        "board": board,
        "page_title": "Nueva etiqueta",
        "screen_title": "Nueva etiqueta",
        "screen_subtitle": "Crea una etiqueta reutilizable dentro del tablero actual.",
        "panel_title": "Nombre de la etiqueta",
        "panel_subtitle": "La etiqueta quedará disponible para las tareas de este tablero.",
        "submit_label": "Guardar etiqueta",
    }
    return render(request, "tasks/task_list_form.html", context)


@login_required
def board_tag_update(request, board_pk, pk):
    tag = _get_owned_tag(request.user, board_pk, pk)
    board = tag.board

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag, board=board)
        if form.is_valid():
            form.save()
            return redirect("board_detail", pk=board.pk)
    else:
        form = TagForm(instance=tag, board=board)

    context = {
        "form": form,
        "board": board,
        "tag": tag,
        "page_title": f"Renombrar {tag.name}",
        "screen_title": "Renombrar etiqueta",
        "screen_subtitle": "Actualiza el nombre de esta etiqueta dentro del tablero actual.",
        "panel_title": "Nombre de la etiqueta",
        "panel_subtitle": "Solo puedes cambiar el nombre; la etiqueta sigue ligada a este tablero.",
        "submit_label": "Guardar cambios",
    }
    return render(request, "tasks/task_list_form.html", context)


@login_required
def board_tag_delete(request, board_pk, pk):
    tag = _get_owned_tag(request.user, board_pk, pk)
    board = tag.board

    if request.method == "POST":
        tag.delete()
        return redirect("board_detail", pk=board.pk)

    context = {
        "board": board,
        "tag": tag,
        "task_count": tag.tasks.count(),
        "page_title": f"Eliminar {tag.name}",
        "screen_title": "Eliminar etiqueta",
        "screen_subtitle": "Confirma si quieres borrar esta etiqueta de forma definitiva.",
        "panel_title": "Confirmación de borrado",
        "panel_subtitle": "Las tareas seguirán existiendo, pero perderán esta etiqueta.",
    }
    return render(request, "tasks/tag_confirm_delete.html", context)


@login_required
def board_task_list_update(request, board_pk, pk):
    task_list = _get_owned_task_list(request.user, board_pk, pk)
    board = task_list.board

    if request.method == "POST":
        form = TaskListForm(request.POST, instance=task_list, board=board)
        if form.is_valid():
            form.save()
            return redirect("board_detail", pk=board.pk)
    else:
        form = TaskListForm(instance=task_list, board=board)

    context = {
        "form": form,
        "board": board,
        "task_list": task_list,
        "page_title": f"Renombrar {task_list.name}",
        "screen_title": "Renombrar lista",
        "screen_subtitle": "Actualiza el nombre de esta lista dentro del tablero actual.",
        "panel_title": "Nombre de la lista",
        "panel_subtitle": "Solo puedes cambiar el nombre; el tablero y la posición actual se mantienen en servidor.",
        "submit_label": "Guardar cambios",
    }
    return render(request, "tasks/task_list_form.html", context)


@login_required
def board_task_list_delete(request, board_pk, pk):
    task_list = _get_owned_task_list(request.user, board_pk, pk)
    board = task_list.board

    if request.method == "POST":
        task_list.delete()
        return redirect("board_detail", pk=board.pk)

    context = {
        "board": board,
        "task_list": task_list,
        "task_count": task_list.tasks.count(),
        "page_title": f"Eliminar {task_list.name}",
        "screen_title": "Eliminar lista",
        "screen_subtitle": "Confirma si quieres borrar esta lista de forma definitiva.",
        "panel_title": "Confirmación de borrado",
        "panel_subtitle": "Las tareas asociadas a esta lista se eliminarán junto con ella.",
    }
    return render(request, "tasks/task_list_confirm_delete.html", context)


@login_required
def board_detail(request, pk):
    board = _get_owned_board_with_tasks(request.user, pk)
    return render(
        request,
        "tasks/board_detail.html",
        _build_board_detail_context(board),
    )


@login_required
def board_export_csv(request, pk):
    board = get_object_or_404(
        Board.objects.filter(owner=request.user).only("pk", "name"),
        pk=pk,
    )
    tasks_queryset = (
        Task.objects.filter(task_list__board=board)
        .select_related("task_list", "assignee")
        .prefetch_related("tags")
        .order_by("task_list__position", "position", "pk")
    )

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="board-{board.pk}-tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "tablero",
            "lista",
            "titulo",
            "descripcion",
            "prioridad",
            "fecha_limite",
            "asignada_a",
            "etiquetas",
        ]
    )

    for task in tasks_queryset:
        writer.writerow(
            [
                board.name,
                task.task_list.name,
                task.title,
                task.description or "",
                task.get_priority_display(),
                task.due_date.isoformat() if task.due_date else "",
                task.assignee.username if task.assignee else "",
                ", ".join(task.tags.order_by("name", "pk").values_list("name", flat=True)),
            ]
        )

    return response


def _get_owned_board_with_tasks(user, board_pk):
    return get_object_or_404(
        Board.objects.filter(owner=user)
        .select_related("owner")
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.order_by("name", "pk"),
            ),
            Prefetch(
                "task_lists",
                queryset=TaskList.objects.prefetch_related(
                    Prefetch(
                        "tasks",
                        queryset=Task.objects.select_related("assignee").prefetch_related("tags").order_by(
                            "position", "pk"
                        ),
                    )
                ).order_by("position", "pk"),
            )
        ),
        pk=board_pk,
    )


def _get_owned_task_list(user, board_pk, task_list_pk):
    return get_object_or_404(
        TaskList.objects.filter(board__owner=user).select_related("board", "board__owner"),
        board_id=board_pk,
        pk=task_list_pk,
    )


def _get_owned_tag(user, board_pk, tag_pk):
    return get_object_or_404(
        Tag.objects.filter(board__owner=user).select_related("board", "board__owner"),
        board_id=board_pk,
        pk=tag_pk,
    )


def _build_task_move_form(board, task, data=None):
    return TaskMoveForm(
        data=data,
        board=board,
        task=task,
        prefix=f"move-{task.pk}",
    )


def _get_next_task_position(task_list):
    max_position = (
        Task.objects.filter(task_list=task_list).aggregate(max_position=Max("position"))["max_position"] or 0
    )
    return max_position + 1


def _get_task_from_board(board, task_pk):
    for task_list in board.task_lists.all():
        for task in task_list.tasks.all():
            if task.pk == task_pk:
                return task
    raise Http404


def _format_compact_due_date_label(due_date):
    if due_date is None:
        return None
    return f"Vence {due_date.day} {SPANISH_MONTH_ABBREVIATIONS[due_date.month]} {due_date.year}"


def _build_board_detail_context(board, *, bound_move_form=None):
    all_tags = list(board.tags.all())
    board_task_lists = []
    for task_list in board.task_lists.all():
        all_tasks = list(task_list.tasks.all())
        for task in all_tasks:
            task.compact_due_date_label = _format_compact_due_date_label(task.due_date)
            if bound_move_form is not None and bound_move_form.task.pk == task.pk:
                task.move_form = bound_move_form
            else:
                task.move_form = _build_task_move_form(board, task)
        total_tasks = len(all_tasks)
        visible_tasks = all_tasks[:5]
        hidden_tasks = all_tasks[5:]
        has_hidden_tasks = total_tasks > 5
        board_task_lists.append(
            {
                "task_list": task_list,
                "total_tasks": total_tasks,
                "visible_tasks": visible_tasks,
                "hidden_tasks": hidden_tasks,
                "has_hidden_tasks": has_hidden_tasks,
            }
        )

    return {
        "board": board,
        "board_visible_tags": all_tags[:3],
        "board_hidden_tags": all_tags[3:],
        "board_has_hidden_tags": len(all_tags) > 3,
        "board_task_lists": board_task_lists,
    }


@login_required
def task_list(request):
    tasks_queryset = (
        Task.objects.filter(task_list__board__owner=request.user)
        .select_related("task_list", "task_list__board", "assignee")
        .prefetch_related("tags")
        .order_by("task_list__board__name", "task_list__position", "position", "pk")
    )
    filter_form = TaskFilterForm(request.GET, user=request.user)
    filter_form.is_valid()

    selected_board = filter_form.cleaned_data["board"]
    selected_task_list = filter_form.cleaned_data["task_list"]
    selected_priority = filter_form.cleaned_data["priority"]

    if selected_board is not None:
        tasks_queryset = tasks_queryset.filter(task_list__board=selected_board)
    if selected_task_list is not None:
        tasks_queryset = tasks_queryset.filter(task_list=selected_task_list)
    if selected_priority:
        tasks_queryset = tasks_queryset.filter(priority=selected_priority)

    paginator = Paginator(tasks_queryset, 5)
    page_number = request.GET.get("page")
    tasks = paginator.get_page(page_number)
    pagination_querystring = _build_task_filter_querystring(
        selected_board=selected_board,
        selected_task_list=selected_task_list,
        selected_priority=selected_priority,
    )
    if pagination_querystring:
        pagination_querystring = f"{pagination_querystring}&"

    context = {
        "tasks": tasks,
        "filter_form": filter_form,
        "pagination_querystring": pagination_querystring,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(
        Task.objects.filter(task_list__board__owner=request.user)
        .select_related("task_list", "task_list__board", "assignee")
        .prefetch_related("tags"),
        pk=pk,
    )
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request, board_pk=None):
    board = None
    preselected_task_list = None
    requested_task_list_pk = request.GET.get("task_list")
    requested_task_list = _get_requested_task_list_for_user(request.user, requested_task_list_pk)
    if board_pk is not None:
        board = get_object_or_404(
            Board.objects.filter(owner=request.user).prefetch_related("task_lists"),
            pk=board_pk,
        )
        if requested_task_list is not None and requested_task_list.board_id == board.pk:
            preselected_task_list = requested_task_list
    elif requested_task_list is not None:
        preselected_task_list = requested_task_list
        board = requested_task_list.board

    if request.method == 'POST':
        form = TaskForm(request.POST, board=board, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.position = _get_next_task_position(task.task_list)
            task.save()
            form.save_m2m()
            return redirect('board_detail', pk=task.task_list.board_id)
    else:
        form_kwargs = {
            "board": board,
            "user": request.user,
        }
        if preselected_task_list is not None:
            form_kwargs["initial"] = {"task_list": preselected_task_list.pk}
        form = TaskForm(**form_kwargs)

    screen_subtitle = 'Crea una nueva tarea dentro del tablero actual.' if board else 'Crea una nueva tarea y asígnala a una lista existente.'
    panel_subtitle = 'Selecciona una de las listas del tablero para guardar la tarea.' if board else 'Completa los campos principales para guardar la tarea.'

    if preselected_task_list is not None:
        screen_subtitle = 'Crea una nueva tarea dentro de la lista seleccionada.'

    context = {
        'form': form,
        'board': board,
        'preselected_task_list': preselected_task_list,
        'page_title': 'Nueva tarea',
        'screen_title': 'Nueva tarea',
        'screen_subtitle': screen_subtitle,
        'panel_title': 'Detalles de la tarea',
        'panel_subtitle': panel_subtitle,
        'submit_label': 'Guardar tarea',
        'cancel_url': 'board_detail' if board else 'board_list',
        'cancel_url_kwargs': {'pk': board.pk} if board else None,
        'task_list_count': form.fields["task_list"].queryset.count(),
        'show_tags': "tags" in form.fields,
        'tag_count': form.fields["tags"].queryset.count() if "tags" in form.fields else 0,
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(
        Task.objects.filter(task_list__board__owner=request.user).select_related("task_list", "task_list__board"),
        pk=pk,
    )
    board = task.task_list.board
    original_task_list_id = task.task_list_id

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, board=board, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            if task.task_list_id != original_task_list_id:
                task.position = _get_next_task_position(task.task_list)
            task.save()
            form.save_m2m()
            return redirect('board_detail', pk=board.pk)
    else:
        form = TaskForm(instance=task, board=board, user=request.user)

    context = {
        'form': form,
        'task': task,
        'board': board,
        'page_title': f'Editar {task.title}',
        'screen_title': 'Editar tarea',
        'screen_subtitle': 'Actualiza esta tarea dentro del tablero actual.',
        'panel_title': 'Editar detalles',
        'panel_subtitle': 'Solo se muestran listas del tablero al que pertenece esta tarea.',
        'submit_label': 'Guardar cambios',
        'cancel_url': 'board_detail',
        'cancel_url_kwargs': {'pk': board.pk},
        'task_list_count': form.fields["task_list"].queryset.count(),
        'show_tags': "tags" in form.fields,
        'tag_count': form.fields["tags"].queryset.count() if "tags" in form.fields else 0,
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(
        Task.objects.filter(task_list__board__owner=request.user).select_related("task_list", "task_list__board"),
        pk=pk,
    )

    if request.method == 'POST':
        board_id = task.task_list.board_id
        task.delete()
        return redirect('board_detail', pk=board_id)

    context = {
        'task': task,
        'page_title': f'Eliminar {task.title}',
        'screen_title': 'Eliminar tarea',
        'screen_subtitle': 'Confirma si quieres borrar esta tarea de forma definitiva.',
        'panel_title': 'Confirmación de borrado',
        'panel_subtitle': 'Si confirmas, esta tarea se eliminará para siempre de su lista actual.',
    }
    return render(request, 'tasks/task_confirm_delete.html', context)


@login_required
def board_task_move(request, board_pk, pk):
    board = _get_owned_board_with_tasks(request.user, board_pk)
    task = _get_task_from_board(board, pk)

    if request.method != "POST":
        return redirect("board_detail", pk=board.pk)

    form = _build_task_move_form(board, task, data=request.POST)
    if form.is_valid():
        task.task_list = form.cleaned_data["task_list"]
        task.position = _get_next_task_position(task.task_list)
        task.save(update_fields=["task_list", "position"])
        return redirect("board_detail", pk=board.pk)

    context = _build_board_detail_context(board, bound_move_form=form)
    return render(request, "tasks/board_detail.html", context, status=200)


def _get_requested_task_list_for_user(user, requested_task_list_pk):
    try:
        requested_task_list_pk = int(requested_task_list_pk)
    except (TypeError, ValueError):
        return None

    return (
        TaskList.objects.filter(board__owner=user)
        .select_related("board", "board__owner")
        .filter(pk=requested_task_list_pk)
        .first()
    )


def _build_task_filter_querystring(*, selected_board, selected_task_list, selected_priority):
    query_params = []
    if selected_board is not None:
        query_params.append(("board", selected_board.pk))
    if selected_task_list is not None:
        query_params.append(("task_list", selected_task_list.pk))
    if selected_priority:
        query_params.append(("priority", selected_priority))
    return urlencode(query_params)
