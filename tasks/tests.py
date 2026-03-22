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
                "assignee": "",
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
