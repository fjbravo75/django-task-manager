from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'task_list', 'priority', 'assignee', 'due_date', 'tags']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'task_list': 'Lista',
            'priority': 'Prioridad',
            'assignee': 'Asignado a',
            'due_date': 'Fecha límite',
            'tags': 'Etiquetas',
        }
