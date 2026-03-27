from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from tasks.demo_data import (
    DEFAULT_DEMO_PASSWORD,
    DEMO_BOARD_DEFINITIONS,
    DEMO_EMAIL,
    DEMO_FIRST_NAME,
    DEMO_LAST_NAME,
    DEMO_USERNAME,
    get_demo_totals,
)
from tasks.models import Board, Tag, Task, TaskList


class Command(BaseCommand):
    help = "Create or refresh the reproducible demo workspace."

    def handle(self, *args, **options):
        demo_password = getattr(settings, "DEMO_USER_PASSWORD", DEFAULT_DEMO_PASSWORD)
        if not demo_password:
            raise CommandError("DEMO_USER_PASSWORD no puede estar vacia.")

        with transaction.atomic():
            demo_user, user_created = self._get_or_create_demo_user(demo_password)
            self._sync_demo_workspace(demo_user)

        totals = get_demo_totals()
        state_label = "creado" if user_created else "actualizado"
        self.stdout.write(
            self.style.SUCCESS(
                f"Espacio demo {state_label}: {totals['boards']} tableros, "
                f"{totals['task_lists']} listas y {totals['tasks']} tareas."
            )
        )
        self.stdout.write(f"Usuario demo: {DEMO_USERNAME}")
        self.stdout.write(f"Contrasena demo: {demo_password}")

    def _get_or_create_demo_user(self, demo_password):
        user_model = get_user_model()
        existing_user = user_model.objects.filter(username=DEMO_USERNAME).first()

        if existing_user and not self._is_managed_demo_user(existing_user):
            raise CommandError(
                "Ya existe un usuario 'demo' ajeno al espacio demo gestionado por "
                "seed_demo. Renombralo o eliminalo manualmente antes de continuar."
            )

        if existing_user is None:
            existing_user = user_model(
                username=DEMO_USERNAME,
                email=DEMO_EMAIL,
                first_name=DEMO_FIRST_NAME,
                last_name=DEMO_LAST_NAME,
                is_active=True,
            )
            user_created = True
        else:
            user_created = False

        existing_user.email = DEMO_EMAIL
        existing_user.first_name = DEMO_FIRST_NAME
        existing_user.last_name = DEMO_LAST_NAME
        existing_user.is_active = True
        existing_user.set_password(demo_password)
        existing_user.save()

        return existing_user, user_created

    def _is_managed_demo_user(self, user):
        return (
            user.email == DEMO_EMAIL
            and user.first_name == DEMO_FIRST_NAME
            and user.last_name == DEMO_LAST_NAME
        )

    def _sync_demo_workspace(self, demo_user):
        today = timezone.localdate()

        for board_definition in DEMO_BOARD_DEFINITIONS:
            board, _ = Board.objects.update_or_create(
                owner=demo_user,
                name=board_definition.name,
                defaults={"description": board_definition.description},
            )

            task_lists_by_name = {}
            for position, task_list_name in enumerate(board_definition.task_lists, start=1):
                task_list, _ = TaskList.objects.update_or_create(
                    board=board,
                    name=task_list_name,
                    defaults={"position": position},
                )
                task_lists_by_name[task_list_name] = task_list

            tags_by_name = {}
            for tag_name in board_definition.tags:
                tag, _ = Tag.objects.update_or_create(board=board, name=tag_name, defaults={})
                tags_by_name[tag_name] = tag

            for task_definition in board_definition.tasks:
                task, _ = Task.objects.update_or_create(
                    task_list=task_lists_by_name[task_definition.task_list],
                    title=task_definition.title,
                    defaults={
                        "description": task_definition.description,
                        "priority": task_definition.priority,
                        "due_date": task_definition.resolve_due_date(today),
                        "assignee": demo_user if task_definition.assign_to_demo else None,
                    },
                )
                task.tags.set([tags_by_name[tag_name] for tag_name in task_definition.tags])
