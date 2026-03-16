from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'status': 'Estado',
            'priority': 'Prioridad',
        }
