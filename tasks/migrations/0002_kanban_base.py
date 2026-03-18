from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_existing_tasks_to_task_lists(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    Board = apps.get_model("tasks", "Board")
    TaskList = apps.get_model("tasks", "TaskList")
    user_app_label, user_model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(user_app_label, user_model_name)

    if not Task.objects.exists():
        return

    owner = User.objects.order_by("pk").first()
    if owner is None:
        username_field = getattr(User, "USERNAME_FIELD", "username")
        owner = User.objects.create(**{username_field: "legacy_owner", "password": "!"})

    board = Board.objects.create(
        name="Migracion inicial",
        description="Tablero generado automaticamente para conservar las tareas existentes.",
        owner=owner,
    )
    board.members.add(owner)

    pending_list = TaskList.objects.create(board=board, name="Pendiente", position=1)
    in_progress_list = TaskList.objects.create(board=board, name="En progreso", position=2)
    done_list = TaskList.objects.create(board=board, name="Hecha", position=3)

    list_by_status = {
        "pending": pending_list,
        "in_progress": in_progress_list,
        "done": done_list,
    }

    for task in Task.objects.all():
        target_list = list_by_status.get(task.status, pending_list)
        task.task_list_id = target_list.id
        task.save(update_fields=["task_list"])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_boards",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(blank=True, related_name="boards", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["name", "pk"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to="tasks.board",
                    ),
                ),
            ],
            options={
                "ordering": ["board_id", "name", "pk"],
            },
        ),
        migrations.CreateModel(
            name="TaskList",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("position", models.PositiveIntegerField(default=0)),
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_lists",
                        to="tasks.board",
                    ),
                ),
            ],
            options={
                "ordering": ["board_id", "position", "pk"],
            },
        ),
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["pk"]},
        ),
        migrations.AddField(
            model_name="task",
            name="assignee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_tasks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[("low", "Baja"), ("medium", "Media"), ("high", "Alta")],
                default="medium",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="tasks", to="tasks.tag"),
        ),
        migrations.AddField(
            model_name="task",
            name="task_list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="tasks.tasklist",
            ),
        ),
        migrations.RunPython(migrate_existing_tasks_to_task_lists, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="task",
            name="status",
        ),
        migrations.AlterField(
            model_name="task",
            name="task_list",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="tasks.tasklist",
            ),
        ),
        migrations.AddConstraint(
            model_name="tag",
            constraint=models.UniqueConstraint(fields=("board", "name"), name="unique_tag_name_per_board"),
        ),
        migrations.AddConstraint(
            model_name="tasklist",
            constraint=models.UniqueConstraint(
                fields=("board", "name"),
                name="unique_task_list_name_per_board",
            ),
        ),
    ]
