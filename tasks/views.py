from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from tasks.forms import TaskForm
from tasks.models import Task


def task_list(request):
    task_list = (
        Task.objects.select_related("task_list", "task_list__board", "assignee")
        .prefetch_related("tags")
        .order_by("task_list__board__name", "task_list__position", "pk")
    )
    paginator = Paginator(task_list, 5)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    task = get_object_or_404(
        Task.objects.select_related("task_list", "task_list__board", "assignee").prefetch_related("tags"),
        pk=pk,
    )
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    context = {
        'form': form,
        'page_title': 'Nueva tarea',
        'screen_title': 'Nueva tarea',
        'screen_subtitle': 'Crea una nueva tarea y asígnala a una lista existente.',
        'panel_title': 'Detalles de la tarea',
        'panel_subtitle': 'Completa los campos principales para guardar la tarea dentro de una lista del tablero.',
        'submit_label': 'Guardar tarea',
        'cancel_url': 'task_list',
    }
    return render(request, 'tasks/task_form.html', context)


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task,
        'page_title': f'Editar {task.title}',
        'screen_title': 'Editar tarea',
        'screen_subtitle': 'Actualiza la tarea y mueve su lista si hace falta.',
        'panel_title': 'Editar detalles',
        'panel_subtitle': 'Modifica los campos necesarios y guarda los cambios en la estructura actual.',
        'submit_label': 'Guardar cambios',
        'cancel_url': 'task_detail',
        'cancel_url_kwargs': {'pk': task.pk},
    }
    return render(request, 'tasks/task_form.html', context)


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    context = {
        'task': task,
        'page_title': f'Eliminar {task.title}',
        'screen_title': 'Eliminar tarea',
        'screen_subtitle': 'Confirma si quieres borrar esta tarea de forma definitiva.',
        'panel_title': 'Confirmación de borrado',
        'panel_subtitle': 'Si confirmas, esta tarea se eliminará para siempre de su lista actual.',
    }
    return render(request, 'tasks/task_confirm_delete.html', context)
