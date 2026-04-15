from django.db import migrations, models


def backfill_task_positions(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    TaskList = apps.get_model("tasks", "TaskList")

    for task_list in TaskList.objects.order_by("board_id", "position", "pk").iterator():
        tasks = list(Task.objects.filter(task_list=task_list).order_by("pk"))
        if not tasks:
            continue

        for position, task in enumerate(tasks, start=1):
            task.position = position

        Task.objects.bulk_update(tasks, ["position"])


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_kanban_base"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="position",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["task_list_id", "position", "pk"]},
        ),
        migrations.RunPython(backfill_task_positions, migrations.RunPython.noop),
    ]
