from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from tasks.forms import BoardForm, RegisterForm, TaskForm
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
        "screen_subtitle": "Crea el tablero principal desde la interfaz web para empezar a organizar tu trabajo.",
        "panel_title": "Detalles del tablero",
        "panel_subtitle": "Define el nombre y una breve descripción inicial del tablero.",
        "submit_label": "Guardar tablero",
    }
    return render(request, "tasks/board_form.html", context)


@login_required
def board_detail(request, pk):
    board = get_object_or_404(
        Board.objects.filter(owner=request.user)
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
        pk=pk,
    )
    return render(request, "tasks/board_detail.html", {"board": board})


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
    if board_pk is not None:
        board = get_object_or_404(
            Board.objects.filter(owner=request.user).prefetch_related("task_lists"),
            pk=board_pk,
        )

    if request.method == 'POST':
        form = TaskForm(request.POST, board=board, user=request.user)
        if form.is_valid():
            task = form.save()
            return redirect('board_detail', pk=task.task_list.board_id)
    else:
        form = TaskForm(board=board, user=request.user)

    context = {
        'form': form,
        'board': board,
        'page_title': 'Nueva tarea',
        'screen_title': 'Nueva tarea',
        'screen_subtitle': 'Crea una nueva tarea dentro del tablero actual.' if board else 'Crea una nueva tarea y asígnala a una lista existente.',
        'panel_title': 'Detalles de la tarea',
        'panel_subtitle': 'Selecciona una de las listas del tablero actual para guardar la tarea.' if board else 'Completa los campos principales para guardar la tarea dentro de una lista del tablero.',
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
        'screen_subtitle': 'Actualiza la tarea dentro del tablero actual.',
        'panel_title': 'Editar detalles',
        'panel_subtitle': 'Solo se muestran listas del tablero al que ya pertenece esta tarea.',
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
