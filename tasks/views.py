from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator
from django.db.models import Max, Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from tasks.forms import BoardForm, RegisterForm, TaskForm, TaskListForm, TaskMoveForm
from tasks.models import Board, Task, TaskList


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
    }
    return render(request, "tasks/board_form.html", context)


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


def _get_owned_board_with_tasks(user, board_pk):
    return get_object_or_404(
        Board.objects.filter(owner=user)
        .select_related("owner")
        .prefetch_related(
            Prefetch(
                "task_lists",
                queryset=TaskList.objects.prefetch_related(
                    Prefetch(
                        "tasks",
                        queryset=Task.objects.select_related("assignee").prefetch_related("tags").order_by("pk"),
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


def _build_task_move_form(board, task, data=None):
    return TaskMoveForm(
        data=data,
        board=board,
        task=task,
        prefix=f"move-{task.pk}",
    )


def _get_task_from_board(board, task_pk):
    for task_list in board.task_lists.all():
        for task in task_list.tasks.all():
            if task.pk == task_pk:
                return task
    raise Http404


def _build_board_detail_context(board, *, bound_move_form=None):
    board_task_lists = []
    for task_list in board.task_lists.all():
        all_tasks = list(task_list.tasks.all())
        for task in all_tasks:
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
        "board_task_lists": board_task_lists,
    }


@login_required
def task_list(request):
    task_list = (
        Task.objects.filter(task_list__board__owner=request.user)
        .select_related("task_list", "task_list__board", "assignee")
        .prefetch_related("tags")
        .order_by("task_list__board__name", "task_list__position", "pk")
    )
    paginator = Paginator(task_list, 5)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


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
    if board_pk is not None:
        board = get_object_or_404(
            Board.objects.filter(owner=request.user).prefetch_related("task_lists"),
            pk=board_pk,
        )
        requested_task_list_pk = request.GET.get("task_list")
        if requested_task_list_pk:
            try:
                requested_task_list_pk = int(requested_task_list_pk)
            except (TypeError, ValueError):
                requested_task_list_pk = None

        if requested_task_list_pk is not None:
            preselected_task_list = board.task_lists.filter(pk=requested_task_list_pk).first()

    if request.method == 'POST':
        form = TaskForm(request.POST, board=board, user=request.user)
        if form.is_valid():
            task = form.save()
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
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(
        Task.objects.filter(task_list__board__owner=request.user).select_related("task_list", "task_list__board"),
        pk=pk,
    )
    board = task.task_list.board

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, board=board, user=request.user)
        if form.is_valid():
            form.save()
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
        task.save()
        return redirect("board_detail", pk=board.pk)

    context = _build_board_detail_context(board, bound_move_form=form)
    return render(request, "tasks/board_detail.html", context, status=200)
