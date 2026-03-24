from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Board, Task, TaskList


class BoardTaskAuthorizationTests(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username="alice", password="testpass123")
        self.user_b = User.objects.create_user(username="bob", password="testpass123")

        self.board_a = Board.objects.create(name="Board A", owner=self.user_a)
        self.board_b = Board.objects.create(name="Board B", owner=self.user_b)

        self.todo_a = TaskList.objects.create(board=self.board_a, name="Todo", position=1)
        self.todo_b = TaskList.objects.create(board=self.board_b, name="Todo", position=1)

        self.task_a = Task.objects.create(title="Task A", task_list=self.todo_a)
        self.task_b = Task.objects.create(title="Task B", task_list=self.todo_b)

    def test_board_list_requires_authentication(self):
        response = self.client.get(reverse("board_list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_list"), response.url)

    def test_board_list_shows_only_authenticated_users_boards(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Board A")
        self.assertNotContains(response, "Board B")
        self.assertContains(response, reverse("board_create"))
        self.assertContains(response, "Nuevo tablero")

    def test_empty_board_list_shows_create_cta_without_admin_dependency(self):
        user_c = User.objects.create_user(username="carol", password="testpass123")
        self.client.force_login(user_c)

        response = self.client.get(reverse("board_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todavía no hay tableros")
        self.assertContains(response, reverse("board_create"))
        self.assertContains(response, "Crear tablero")
        self.assertNotContains(response, "Ir al admin")
        self.assertNotContains(response, "/admin/")

    def test_board_create_requires_authentication(self):
        response = self.client.get(reverse("board_create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_create"), response.url)

    def test_board_create_form_only_exposes_name_and_description(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_create"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["form"].fields.keys()), ["name", "description"])

    def test_board_detail_shows_task_list_create_cta(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("board_task_list_create", args=[self.board_a.pk]))
        self.assertContains(response, "Nueva lista")

    def test_board_create_assigns_owner_in_server_and_redirects_to_detail(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_create"),
            {
                "name": "Roadmap 2026",
                "description": "Board created from the UI",
                "owner": self.user_b.pk,
            },
        )

        board = Board.objects.get(name="Roadmap 2026")

        self.assertEqual(board.owner, self.user_a)
        self.assertNotEqual(board.owner, self.user_b)
        self.assertRedirects(response, reverse("board_detail", args=[board.pk]))

        board_list_response = self.client.get(reverse("board_list"))
        self.assertContains(board_list_response, "Roadmap 2026")

        self.client.force_login(self.user_b)
        foreign_detail_response = self.client.get(reverse("board_detail", args=[board.pk]))
        self.assertEqual(foreign_detail_response.status_code, 404)

    def test_user_cannot_open_board_detail_for_foreign_board(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_b.pk]))

        self.assertEqual(response.status_code, 404)

    def test_task_list_shows_only_tasks_from_users_boards(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task A")
        self.assertNotContains(response, "Task B")

    def test_user_cannot_access_foreign_task_urls(self):
        self.client.force_login(self.user_a)

        foreign_task_urls = [
            reverse("task_detail", args=[self.task_b.pk]),
            reverse("task_update", args=[self.task_b.pk]),
            reverse("task_delete", args=[self.task_b.pk]),
        ]

        for url in foreign_task_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_foreign_task_by_post(self):
        self.client.force_login(self.user_a)

        response = self.client.post(reverse("task_delete", args=[self.task_b.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.task_b.pk).exists())

    def test_board_task_create_rejects_foreign_board(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_create", args=[self.board_b.pk]))

        self.assertEqual(response.status_code, 404)

    def test_board_task_list_create_requires_authentication(self):
        response = self.client.get(reverse("board_task_list_create", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_task_list_create", args=[self.board_a.pk]), response.url)

    def test_board_task_list_create_rejects_foreign_board(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_list_create", args=[self.board_b.pk]))

        self.assertEqual(response.status_code, 404)

    def test_board_task_list_create_form_only_exposes_name(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_list_create", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["form"].fields.keys()), ["name"])
        self.assertContains(response, self.board_a.name)

    def test_board_task_list_create_assigns_board_and_position_in_server_and_redirects(self):
        self.client.force_login(self.user_a)
        TaskList.objects.create(board=self.board_a, name="Doing", position=5)

        response = self.client.post(
            reverse("board_task_list_create", args=[self.board_a.pk]),
            {
                "name": "Done",
                "board": self.board_b.pk,
                "position": 999,
            },
        )

        task_list = TaskList.objects.get(board=self.board_a, name="Done")

        self.assertEqual(task_list.board, self.board_a)
        self.assertNotEqual(task_list.board, self.board_b)
        self.assertEqual(task_list.position, 6)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        self.assertContains(board_detail_response, "Done")

    def test_board_task_list_create_rejects_duplicate_name_within_same_board(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_list_create", args=[self.board_a.pk]),
            {
                "name": "Todo",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TaskList.objects.filter(board=self.board_a, name="Todo").count(), 1)
        self.assertIn("name", response.context["form"].errors)

    def test_board_detail_shows_task_create_cta_for_each_task_list(self):
        empty_task_list = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'{reverse("board_task_create", args=[self.board_a.pk])}?task_list={self.todo_a.pk}',
        )
        self.assertContains(
            response,
            f'{reverse("board_task_create", args=[self.board_a.pk])}?task_list={empty_task_list.pk}',
        )
        self.assertContains(response, "Crear la primera tarea")

    def test_board_task_create_preselects_task_list_from_query_param(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        self.client.force_login(self.user_a)

        response = self.client.get(
            f'{reverse("board_task_create", args=[self.board_a.pk])}?task_list={doing.pk}',
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(list(form.fields["task_list"].queryset), [self.todo_a, doing])
        self.assertEqual(form.initial["task_list"], doing.pk)
        self.assertEqual(response.context["preselected_task_list"], doing)
        self.assertEqual(
            response.context["panel_subtitle"],
            "Selecciona una de las listas del tablero para guardar la tarea.",
        )
        self.assertContains(
            response,
            "La lista llega preseleccionada, pero puedes cambiarla dentro de este tablero.",
            count=1,
        )

    def test_board_task_create_form_does_not_expose_assignee(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_create", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("task_list", form.fields)
        self.assertIn("priority", form.fields)
        self.assertIn("due_date", form.fields)
        self.assertIn("tags", form.fields)
        self.assertNotIn("assignee", form.fields)
        self.assertNotContains(response, "Asignado a")
        self.assertContains(response, "Solo se muestran listas del tablero actual.")

    def test_board_task_create_ignores_task_list_query_param_from_another_board(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_task_list = TaskList.objects.create(board=other_board, name="Later", position=1)
        self.client.force_login(self.user_a)

        response = self.client.get(
            f'{reverse("board_task_create", args=[self.board_a.pk])}?task_list={other_task_list.pk}',
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertNotIn("task_list", form.initial)
        self.assertIsNone(response.context["preselected_task_list"])
        self.assertContains(response, "Solo se muestran listas del tablero actual.")

    def test_board_task_create_creates_task_in_selected_list_and_redirects_to_detail(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            f'{reverse("board_task_create", args=[self.board_a.pk])}?task_list={self.todo_a.pk}',
            {
                "title": "Plan de release",
                "description": "Cerrar la tarea desde el tablero",
                "task_list": self.todo_a.pk,
                "priority": Task.PRIORITY_HIGH,
                "due_date": "",
                "tags": [],
            },
        )

        task = Task.objects.get(title="Plan de release")

        self.assertEqual(task.task_list, self.todo_a)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        self.assertContains(board_detail_response, "Plan de release")

    def test_board_task_create_rejects_task_list_from_another_board_same_owner(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_task_list = TaskList.objects.create(board=other_board, name="Later", position=1)
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_create", args=[self.board_a.pk]),
            {
                "title": "Wrong board task",
                "description": "",
                "task_list": other_task_list.pk,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("task_list", form.errors)
        self.assertTrue(
            any("Select a valid choice." in error for error in form.errors["task_list"]),
        )
        self.assertFalse(Task.objects.filter(title="Wrong board task").exists())

    def test_board_task_create_for_board_without_lists_keeps_existing_empty_state(self):
        board_without_lists = Board.objects.create(name="Board Empty", owner=self.user_a)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_create", args=[board_without_lists.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task_list_count"], 0)
        self.assertContains(response, "Este tablero aún no tiene listas. Añade una lista antes de crear tareas.")

    def test_task_update_form_does_not_expose_assignee(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_update", args=[self.task_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("assignee", response.context["form"].fields)
        self.assertNotContains(response, "Asignado a")

    def test_board_detail_shows_priority_badge_and_task_actions_for_visible_task(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_a.get_priority_display())
        self.assertContains(response, reverse("task_detail", args=[self.task_a.pk]))
        self.assertContains(response, reverse("task_update", args=[self.task_a.pk]))

    def test_task_create_form_only_exposes_owned_task_lists(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_create"))

        self.assertEqual(response.status_code, 200)
        task_list_field = response.context["form"].fields["task_list"]
        self.assertEqual(list(task_list_field.queryset), [self.todo_a])

    def test_task_create_rejects_foreign_task_list_submission(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("task_create"),
            {
                "title": "Intrusion attempt",
                "description": "",
                "task_list": self.todo_b.pk,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("task_list", form.errors)
        self.assertTrue(
            any("Select a valid choice." in error for error in form.errors["task_list"]),
        )
        self.assertFalse(Task.objects.filter(title="Intrusion attempt").exists())
