import csv
from datetime import date
from io import StringIO

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Board, Tag, Task, TaskList


class AuthenticationFlowTests(TestCase):
    def test_login_get_for_anonymous_user_renders_login_template(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertContains(response, "Bienvenido a Gestor de tareas")
        self.assertContains(response, "Organiza tu trabajo con claridad")
        self.assertContains(
            response,
            "Reúne tus tableros, listas y tareas en un solo lugar. Ordena prioridades, sigue cada avance y mantén el foco sin complicarte.",
        )
        self.assertContains(response, "Tableros claros para cada proyecto")
        self.assertContains(response, "Listas y tareas fáciles de revisar")
        self.assertContains(response, "Prioridades y fechas visibles de un vistazo")
        self.assertContains(response, "Entra y sigue por donde lo dejaste.")

    def test_login_shows_labels_in_spanish(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<label for=\"id_username\">Usuario</label>", html=True)
        self.assertContains(response, "<label for=\"id_password\">Contraseña</label>", html=True)

    def test_authenticated_user_is_redirected_away_from_login(self):
        user = User.objects.create_user(username="alice", password="testpass123")
        self.client.force_login(user)

        response = self.client.get(reverse("login"))

        self.assertRedirects(response, reverse("board_list"))

    def test_login_with_invalid_credentials_shows_clear_error_message(self):
        User.objects.create_user(username="alice", password="testpass123")

        response = self.client.post(
            reverse("login"),
            {
                "username": "alice",
                "password": "wrongpass",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertContains(
            response,
            "No hemos podido iniciar sesión con esos datos. Revisa tu usuario y tu contraseña e inténtalo de nuevo.",
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_register_get_for_anonymous_user_renders_register_template(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "Bienvenido a Gestor de tareas")
        self.assertContains(response, "Crea tu espacio de trabajo")
        self.assertContains(
            response,
            "Empieza con una cuenta propia para gestionar proyectos, listas y tareas desde una interfaz clara y directa. Todo preparado para que puedas organizarte sin dar rodeos.",
        )
        self.assertContains(response, "Tableros para cada proyecto")
        self.assertContains(response, "Seguimiento claro de tareas")
        self.assertContains(response, "Prioridades y fechas siempre visibles")
        self.assertContains(response, "Crea tu cuenta y empieza a organizarte.")
        self.assertContains(response, "Hasta 50 caracteres. Puedes usar letras, números y @/./+/-/_.")
        self.assertContains(response, "Tu contraseña debe contener al menos 8 caracteres.")
        self.assertContains(response, "Repite la misma contraseña para confirmar que la has escrito bien.")

    def test_register_valid_post_creates_user_logs_them_in_and_redirects(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "maria",
                "password1": "ClaveSegura123",
                "password2": "ClaveSegura123",
            },
        )

        user = User.objects.get(username="maria")

        self.assertRedirects(response, reverse("board_list"))
        self.assertEqual(self.client.session.get("_auth_user_id"), str(user.pk))

    def test_register_invalid_post_shows_mismatch_error_in_spanish(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "maria",
                "password1": "ClaveSegura123",
                "password2": "OtraClave123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(
            response,
            "Las contraseñas no coinciden. Revisa ambos campos y vuelve a intentarlo.",
        )

    def test_register_invalid_post_shows_password_validator_error_in_spanish(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "maria",
                "password1": "123",
                "password2": "123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(
            response,
            "La contraseña es demasiado corta. Debe contener por lo menos 8 caracteres.",
        )

    def test_register_invalid_post_shows_duplicate_username_error_in_spanish(self):
        User.objects.create_user(username="maria", password="testpass123")

        response = self.client.post(
            reverse("register"),
            {
                "username": "maria",
                "password1": "ClaveSegura123",
                "password2": "ClaveSegura123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(
            response,
            "Ya existe una cuenta con ese nombre de usuario. Prueba con otro.",
        )

    def test_logout_logs_user_out_and_redirects_to_login(self):
        user = User.objects.create_user(username="alice", password="testpass123")
        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)


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

    def test_board_update_requires_authentication(self):
        response = self.client.get(reverse("board_update", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_update", args=[self.board_a.pk]), response.url)

    def test_board_update_rejects_foreign_board(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_update", args=[self.board_b.pk]))

        self.assertEqual(response.status_code, 404)

    def test_board_update_form_only_exposes_name_and_description(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_update", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["form"].fields.keys()), ["name", "description"])
        self.assertContains(response, "Editar tablero")

    def test_board_update_keeps_owner_in_server_and_redirects_to_detail(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_update", args=[self.board_a.pk]),
            {
                "name": "Board A Renamed",
                "description": "Updated from the UI",
                "owner": self.user_b.pk,
            },
        )

        self.board_a.refresh_from_db()

        self.assertEqual(self.board_a.name, "Board A Renamed")
        self.assertEqual(self.board_a.description, "Updated from the UI")
        self.assertEqual(self.board_a.owner, self.user_a)
        self.assertNotEqual(self.board_a.owner, self.user_b)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        self.assertContains(board_detail_response, "Board A Renamed")

    def test_board_delete_requires_authentication(self):
        response = self.client.get(reverse("board_delete", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_delete", args=[self.board_a.pk]), response.url)

    def test_board_delete_rejects_foreign_board(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_delete", args=[self.board_b.pk]))

        self.assertEqual(response.status_code, 404)

    def test_board_delete_renders_confirmation_with_cascade_warning(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_delete", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eliminar tablero")
        self.assertContains(response, "Confirmar borrado")
        self.assertContains(response, "Listas asociadas")
        self.assertContains(response, "Tareas asociadas")
        self.assertContains(response, "listas y tareas asociadas")
        self.assertContains(response, self.board_a.name)

    def test_board_delete_deletes_board_and_related_data_and_redirects_to_board_list(self):
        self.client.force_login(self.user_a)

        response = self.client.post(reverse("board_delete", args=[self.board_a.pk]))

        self.assertRedirects(response, reverse("board_list"))
        self.assertFalse(Board.objects.filter(pk=self.board_a.pk).exists())
        self.assertFalse(TaskList.objects.filter(pk=self.todo_a.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task_a.pk).exists())

    def test_board_detail_shows_task_list_create_cta(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("board_task_list_create", args=[self.board_a.pk]))
        self.assertContains(response, "Nueva lista")

    def test_board_detail_shows_tag_create_link(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("board_tag_create", args=[self.board_a.pk]))
        self.assertContains(response, "Nueva etiqueta")

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

    def test_task_list_filter_form_shows_only_owned_boards_lists_and_priorities(self):
        own_board = Board.objects.create(name="Board C", owner=self.user_a)
        own_list = TaskList.objects.create(board=own_board, name="Doing", position=1)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)
        form = response.context["filter_form"]
        self.assertEqual(
            list(form.fields["board"].queryset.values_list("pk", flat=True)),
            [self.board_a.pk, own_board.pk],
        )
        self.assertEqual(
            list(form.fields["task_list"].queryset.values_list("pk", flat=True)),
            [self.todo_a.pk, own_list.pk],
        )
        self.assertEqual(list(form.fields["priority"].choices), [("", "Todas"), *Task.PRIORITY_CHOICES])

    def test_task_list_filter_form_limits_task_lists_to_selected_board(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        TaskList.objects.create(board=other_board, name="Review", position=1)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_list"), {"board": self.board_a.pk})

        self.assertEqual(response.status_code, 200)
        form = response.context["filter_form"]
        self.assertEqual(
            list(form.fields["task_list"].queryset.values_list("pk", flat=True)),
            [self.todo_a.pk, doing.pk],
        )

    def test_task_list_can_filter_by_board(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_list = TaskList.objects.create(board=other_board, name="Doing", position=1)
        Task.objects.create(title="Task C", task_list=other_list)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_list"), {"board": self.board_a.pk})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task A")
        self.assertNotContains(response, "Task C")
        self.assertNotContains(response, "Task B")

    def test_task_list_can_filter_by_task_list_within_selected_board(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        Task.objects.create(title="Task Doing", task_list=doing)
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_list = TaskList.objects.create(board=other_board, name="Review", position=1)
        Task.objects.create(title="Task Review", task_list=other_list)
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("task_list"),
            {"board": self.board_a.pk, "task_list": doing.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task Doing")
        self.assertNotContains(response, "Task A")
        self.assertNotContains(response, "Task Review")
        self.assertNotContains(response, "Task B")

    def test_task_list_can_filter_by_priority(self):
        self.task_a.priority = Task.PRIORITY_HIGH
        self.task_a.save(update_fields=["priority"])
        own_medium_task = Task.objects.create(
            title="Task Medium",
            task_list=self.todo_a,
            priority=Task.PRIORITY_MEDIUM,
        )
        self.task_b.priority = Task.PRIORITY_HIGH
        self.task_b.save(update_fields=["priority"])
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_list"), {"priority": Task.PRIORITY_HIGH})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_a.title)
        self.assertNotContains(response, own_medium_task.title)
        self.assertNotContains(response, self.task_b.title)

    def test_task_list_can_filter_by_board_task_list_and_priority_together(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        target_task = Task.objects.create(
            title="Task Critical Todo",
            task_list=self.todo_a,
            priority=Task.PRIORITY_HIGH,
        )
        Task.objects.create(
            title="Task Medium Todo",
            task_list=self.todo_a,
            priority=Task.PRIORITY_MEDIUM,
        )
        Task.objects.create(
            title="Task Critical Doing",
            task_list=doing,
            priority=Task.PRIORITY_HIGH,
        )
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_list = TaskList.objects.create(board=other_board, name="Review", position=1)
        Task.objects.create(
            title="Task Critical Review",
            task_list=other_list,
            priority=Task.PRIORITY_HIGH,
        )
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("task_list"),
            {
                "board": self.board_a.pk,
                "task_list": self.todo_a.pk,
                "priority": Task.PRIORITY_HIGH,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, target_task.title)
        self.assertNotContains(response, "Task Medium Todo")
        self.assertNotContains(response, "Task Critical Doing")
        self.assertNotContains(response, "Task Critical Review")
        self.assertNotContains(response, "Task B")

    def test_task_list_pagination_preserves_active_filter_querystring(self):
        self.task_a.priority = Task.PRIORITY_HIGH
        self.task_a.save(update_fields=["priority"])
        for index in range(5):
            Task.objects.create(
                title=f"Task High {index}",
                task_list=self.todo_a,
                priority=Task.PRIORITY_HIGH,
            )
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("task_list"),
            {"board": self.board_a.pk, "priority": Task.PRIORITY_HIGH},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="?board={self.board_a.pk}&amp;priority={Task.PRIORITY_HIGH}&amp;page=2"',
            html=False,
        )

    def test_task_list_ignores_invalid_or_foreign_filter_params_safely(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_list = TaskList.objects.create(board=other_board, name="Review", position=1)
        Task.objects.create(title="Task Review", task_list=other_list)
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("task_list"),
            {
                "board": self.board_b.pk,
                "task_list": self.todo_b.pk,
                "priority": "urgent",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task A")
        self.assertContains(response, "Task Review")
        self.assertNotContains(response, "Task B")
        self.assertFalse(response.context["filter_form"].errors)

    def test_task_list_ignores_task_list_outside_selected_board(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_list = TaskList.objects.create(board=other_board, name="Review", position=1)
        Task.objects.create(title="Task Review", task_list=other_list)
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("task_list"),
            {
                "board": self.board_a.pk,
                "task_list": other_list.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task A")
        self.assertNotContains(response, "Task Review")
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

    def test_task_delete_deletes_owned_task_and_removes_it_from_board_detail(self):
        self.client.force_login(self.user_a)

        response = self.client.post(reverse("task_delete", args=[self.task_a.pk]))

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertFalse(Task.objects.filter(pk=self.task_a.pk).exists())

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        self.assertNotContains(board_detail_response, "Task A")

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

    def test_board_tag_create_requires_authentication(self):
        response = self.client.get(reverse("board_tag_create", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_tag_create", args=[self.board_a.pk]), response.url)

    def test_board_tag_create_rejects_foreign_board(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_tag_create", args=[self.board_b.pk]))

        self.assertEqual(response.status_code, 404)

    def test_board_tag_create_form_only_exposes_name(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_tag_create", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["form"].fields.keys()), ["name"])
        self.assertContains(response, self.board_a.name)

    def test_board_tag_create_assigns_board_in_server_and_redirects(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_tag_create", args=[self.board_a.pk]),
            {
                "name": "Backend",
                "board": self.board_b.pk,
            },
        )

        tag = Tag.objects.get(board=self.board_a, name="Backend")

        self.assertEqual(tag.board, self.board_a)
        self.assertNotEqual(tag.board, self.board_b)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

    def test_board_tag_create_rejects_duplicate_name_within_same_board(self):
        Tag.objects.create(board=self.board_a, name="Backend")
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_tag_create", args=[self.board_a.pk]),
            {
                "name": "Backend",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.objects.filter(board=self.board_a, name="Backend").count(), 1)
        self.assertIn("name", response.context["form"].errors)

    def test_board_tag_update_requires_authentication(self):
        tag = Tag.objects.create(board=self.board_a, name="Backend")

        response = self.client.get(
            reverse("board_tag_update", args=[self.board_a.pk, tag.pk]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_tag_update", args=[self.board_a.pk, tag.pk]), response.url)

    def test_board_tag_update_rejects_foreign_tag(self):
        foreign_tag = Tag.objects.create(board=self.board_b, name="Urgente")
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("board_tag_update", args=[self.board_b.pk, foreign_tag.pk]),
        )

        self.assertEqual(response.status_code, 404)

    def test_board_tag_update_form_only_exposes_name(self):
        tag = Tag.objects.create(board=self.board_a, name="Backend")
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("board_tag_update", args=[self.board_a.pk, tag.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["form"].fields.keys()), ["name"])
        self.assertContains(response, self.board_a.name)
        self.assertContains(response, "Renombrar etiqueta")

    def test_board_tag_update_keeps_board_in_server_and_redirects(self):
        tag = Tag.objects.create(board=self.board_a, name="Backend")
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_tag_update", args=[self.board_a.pk, tag.pk]),
            {
                "name": "API",
                "board": self.board_b.pk,
            },
        )

        tag.refresh_from_db()

        self.assertEqual(tag.name, "API")
        self.assertEqual(tag.board, self.board_a)
        self.assertNotEqual(tag.board, self.board_b)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

    def test_board_tag_update_rejects_duplicate_name_within_same_board(self):
        Tag.objects.create(board=self.board_a, name="Backend")
        tag = Tag.objects.create(board=self.board_a, name="API")
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_tag_update", args=[self.board_a.pk, tag.pk]),
            {
                "name": "Backend",
            },
        )

        tag.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag.name, "API")
        self.assertIn("name", response.context["form"].errors)

    def test_board_tag_delete_requires_authentication(self):
        tag = Tag.objects.create(board=self.board_a, name="Backend")

        response = self.client.get(
            reverse("board_tag_delete", args=[self.board_a.pk, tag.pk]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_tag_delete", args=[self.board_a.pk, tag.pk]), response.url)

    def test_board_tag_delete_rejects_foreign_tag(self):
        foreign_tag = Tag.objects.create(board=self.board_b, name="Urgente")
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_tag_delete", args=[self.board_b.pk, foreign_tag.pk]),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tag.objects.filter(pk=foreign_tag.pk).exists())

    def test_board_tag_delete_renders_confirmation(self):
        tag = Tag.objects.create(board=self.board_a, name="Backend")
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("board_tag_delete", args=[self.board_a.pk, tag.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eliminar etiqueta")
        self.assertContains(response, "Confirmar borrado")
        self.assertContains(response, tag.name)
        self.assertContains(response, "Tareas asociadas")

    def test_board_tag_delete_deletes_tag_but_keeps_tasks_and_clears_relations(self):
        tag = Tag.objects.create(board=self.board_a, name="Backend")
        self.task_a.tags.add(tag)
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_tag_delete", args=[self.board_a.pk, tag.pk]),
        )

        self.task_a.refresh_from_db()

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertFalse(Tag.objects.filter(pk=tag.pk).exists())
        self.assertTrue(Task.objects.filter(pk=self.task_a.pk).exists())
        self.assertFalse(self.task_a.tags.exists())

    def test_board_task_list_update_requires_authentication(self):
        response = self.client.get(
            reverse("board_task_list_update", args=[self.board_a.pk, self.todo_a.pk]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_task_list_update", args=[self.board_a.pk, self.todo_a.pk]), response.url)

    def test_board_task_list_update_rejects_foreign_task_list(self):
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("board_task_list_update", args=[self.board_b.pk, self.todo_b.pk]),
        )

        self.assertEqual(response.status_code, 404)

    def test_board_task_list_update_form_only_exposes_name(self):
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("board_task_list_update", args=[self.board_a.pk, self.todo_a.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["form"].fields.keys()), ["name"])
        self.assertContains(response, self.board_a.name)

    def test_board_task_list_update_keeps_board_and_position_in_server(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_list_update", args=[self.board_a.pk, self.todo_a.pk]),
            {
                "name": "Backlog",
                "board": self.board_b.pk,
                "position": 999,
            },
        )

        self.todo_a.refresh_from_db()

        self.assertEqual(self.todo_a.name, "Backlog")
        self.assertEqual(self.todo_a.board, self.board_a)
        self.assertNotEqual(self.todo_a.board, self.board_b)
        self.assertEqual(self.todo_a.position, 1)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

    def test_board_task_list_update_rejects_duplicate_name_within_same_board(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_list_update", args=[self.board_a.pk, doing.pk]),
            {
                "name": "Todo",
            },
        )

        doing.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(doing.name, "Doing")
        self.assertIn("name", response.context["form"].errors)

    def test_board_task_list_delete_requires_authentication(self):
        response = self.client.get(
            reverse("board_task_list_delete", args=[self.board_a.pk, self.todo_a.pk]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_task_list_delete", args=[self.board_a.pk, self.todo_a.pk]), response.url)

    def test_board_task_list_delete_rejects_foreign_task_list(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_list_delete", args=[self.board_b.pk, self.todo_b.pk]),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(TaskList.objects.filter(pk=self.todo_b.pk).exists())

    def test_board_task_list_delete_renders_confirmation(self):
        self.client.force_login(self.user_a)

        response = self.client.get(
            reverse("board_task_list_delete", args=[self.board_a.pk, self.todo_a.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eliminar lista")
        self.assertContains(response, "Confirmar borrado")
        self.assertContains(response, self.todo_a.name)
        self.assertContains(response, "Tareas asociadas")

    def test_board_task_list_delete_deletes_task_list_and_redirects_to_board_detail(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_list_delete", args=[self.board_a.pk, self.todo_a.pk]),
        )

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertFalse(TaskList.objects.filter(pk=self.todo_a.pk).exists())
        self.assertFalse(Task.objects.filter(pk=self.task_a.pk).exists())

    def test_board_detail_shows_task_list_management_ctas(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("board_task_list_update", args=[self.board_a.pk, self.todo_a.pk]),
        )
        self.assertContains(
            response,
            reverse("board_task_list_delete", args=[self.board_a.pk, self.todo_a.pk]),
        )
        self.assertContains(response, "Editar nombre")
        self.assertContains(response, "Borrar lista")

    def test_board_detail_shows_board_management_ctas(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("board_update", args=[self.board_a.pk]))
        self.assertContains(response, reverse("board_delete", args=[self.board_a.pk]))
        self.assertContains(response, "Editar tablero")
        self.assertContains(response, "Borrar tablero")

    def test_board_detail_shows_action_group_labels_and_export_csv_button(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tablero")
        self.assertContains(response, "Listas")
        self.assertContains(response, "Tareas")
        self.assertContains(response, reverse("board_export_csv", args=[self.board_a.pk]))
        self.assertContains(response, "Exportar CSV")

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

    def test_board_detail_shows_task_move_control_when_board_has_another_list(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("board_task_move", args=[self.board_a.pk, self.task_a.pk]))
        self.assertContains(response, 'name="move-{}-task_list"'.format(self.task_a.pk), html=False)
        self.assertContains(response, doing.name)

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

    def test_board_task_create_form_exposes_owner_only_as_optional_assignee(self):
        tag_a = Tag.objects.create(board=self.board_a, name="Backend")
        Tag.objects.create(board=self.board_b, name="Urgente")
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_create", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("task_list", form.fields)
        self.assertIn("assignee", form.fields)
        self.assertIn("priority", form.fields)
        self.assertIn("due_date", form.fields)
        self.assertIn("tags", form.fields)
        self.assertEqual(list(form.fields["assignee"].queryset), [self.user_a])
        self.assertEqual(form.fields["assignee"].empty_label, "Sin asignar")
        self.assertEqual(list(form.fields["tags"].queryset), [tag_a])
        self.assertContains(response, "Asignada a")
        self.assertContains(response, "Solo se muestran listas del tablero actual.")

    def test_board_task_create_renders_tags_as_checkbox_list_with_multiple_choice_hint(self):
        Tag.objects.create(board=self.board_a, name="Backend")
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_create", args=[self.board_a.pk]))
        form = response.context["form"]

        self.assertEqual(form.fields["tags"].widget.__class__.__name__, "CheckboxSelectMultiple")
        self.assertEqual(form.fields["tags"].widget.attrs["class"], "task-form-tag-checkbox")
        self.assertContains(response, "(marca varias)")
        self.assertContains(response, 'task-form-bottom-grid', html=False)
        self.assertContains(response, 'task-form-bottom-main', html=False)
        self.assertContains(response, 'task-form-bottom-side', html=False)
        self.assertContains(response, 'task-form-tag-select', html=False)
        self.assertContains(response, 'task-form-tag-options', html=False)
        self.assertContains(response, 'task-form-tag-option', html=False)
        self.assertContains(response, 'task-form-tag-option__label', html=False)
        self.assertContains(response, 'task-form-tag-checkbox', html=False)
        self.assertContains(response, 'name="tags"', html=False)
        self.assertContains(response, 'type="checkbox"', html=False)
        self.assertNotContains(response, 'id="id_tags"', html=False)

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

    def test_board_task_create_persists_priority_and_due_date_and_renders_them_across_views(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_create", args=[self.board_a.pk]),
            {
                "title": "Task with due date",
                "description": "Task metadata roundtrip",
                "task_list": self.todo_a.pk,
                "priority": Task.PRIORITY_HIGH,
                "due_date": "2026-03-28",
                "tags": [],
            },
        )

        task = Task.objects.get(title="Task with due date")

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertEqual(task.priority, Task.PRIORITY_HIGH)
        self.assertEqual(task.due_date, date(2026, 3, 28))

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        task_detail_response = self.client.get(reverse("task_detail", args=[task.pk]))
        task_list_response = self.client.get(reverse("task_list"))

        self.assertContains(board_detail_response, "Task with due date")
        self.assertContains(board_detail_response, task.get_priority_display())
        self.assertContains(board_detail_response, "Vence 28 mar 2026")
        self.assertNotContains(board_detail_response, "Fecha límite: 28/03/2026")
        self.assertNotContains(board_detail_response, "bg-amber-100", html=False)
        self.assertNotContains(board_detail_response, "text-amber-700", html=False)

        self.assertContains(task_detail_response, task.get_priority_display())
        self.assertContains(task_detail_response, "28/03/2026")

        self.assertContains(task_list_response, "Task with due date")
        self.assertContains(task_list_response, task.get_priority_display())
        self.assertContains(task_list_response, "Fecha límite: 28/03/2026")

    def test_task_create_with_owned_task_list_query_param_persists_priority_and_due_date(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            f'{reverse("task_create")}?task_list={self.todo_a.pk}',
            {
                "title": "Task created from global form",
                "description": "Board inferred from task list",
                "task_list": self.todo_a.pk,
                "priority": Task.PRIORITY_LOW,
                "due_date": "2026-04-09",
            },
        )

        task = Task.objects.get(title="Task created from global form")

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertEqual(task.task_list, self.todo_a)
        self.assertEqual(task.priority, Task.PRIORITY_LOW)
        self.assertEqual(task.due_date, date(2026, 4, 9))

    def test_board_task_create_creates_task_with_assignee(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_create", args=[self.board_a.pk]),
            {
                "title": "Task with assignee",
                "description": "",
                "task_list": self.todo_a.pk,
                "assignee": self.user_a.pk,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [],
            },
        )

        task = Task.objects.get(title="Task with assignee")

        self.assertEqual(task.task_list, self.todo_a)
        self.assertEqual(task.assignee, self.user_a)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

    def test_board_task_create_rejects_assignee_outside_allowed_queryset(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_create", args=[self.board_a.pk]),
            {
                "title": "Task with invalid assignee",
                "description": "",
                "task_list": self.todo_a.pk,
                "assignee": self.user_b.pk,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("assignee", response.context["form"].errors)
        self.assertFalse(Task.objects.filter(title="Task with invalid assignee").exists())

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

    def test_board_task_create_rejects_tag_from_another_board_same_owner(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_tag = Tag.objects.create(board=other_board, name="Later")
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_create", args=[self.board_a.pk]),
            {
                "title": "Wrong board tag",
                "description": "",
                "task_list": self.todo_a.pk,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [other_tag.pk],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("tags", response.context["form"].errors)
        self.assertFalse(Task.objects.filter(title="Wrong board tag").exists())

    def test_board_task_create_for_board_without_lists_keeps_existing_empty_state(self):
        board_without_lists = Board.objects.create(name="Board Empty", owner=self.user_a)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_task_create", args=[board_without_lists.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task_list_count"], 0)
        self.assertContains(response, "Este tablero aún no tiene listas. Añade una lista antes de crear tareas.")

    def test_task_update_form_exposes_owner_only_as_optional_assignee(self):
        tag_a = Tag.objects.create(board=self.board_a, name="Backend")
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        Tag.objects.create(board=other_board, name="Later")
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_update", args=[self.task_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["form"].fields["assignee"].queryset), [self.user_a])
        self.assertEqual(response.context["form"].fields["assignee"].empty_label, "Sin asignar")
        self.assertEqual(list(response.context["form"].fields["tags"].queryset), [tag_a])
        self.assertContains(response, "Asignada a")

    def test_task_update_assigns_task_to_board_owner(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("task_update", args=[self.task_a.pk]),
            {
                "title": "Task A",
                "description": "Updated from the UI",
                "task_list": self.todo_a.pk,
                "assignee": self.user_a.pk,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [],
            },
        )

        self.task_a.refresh_from_db()

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertEqual(self.task_a.assignee, self.user_a)

    def test_task_update_persists_priority_and_modified_due_date_and_renders_updated_values(self):
        self.task_a.priority = Task.PRIORITY_LOW
        self.task_a.due_date = date(2026, 1, 10)
        self.task_a.save(update_fields=["priority", "due_date"])
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("task_update", args=[self.task_a.pk]),
            {
                "title": "Task A",
                "description": "Updated metadata from the UI",
                "task_list": self.todo_a.pk,
                "priority": Task.PRIORITY_HIGH,
                "due_date": "2026-04-12",
                "tags": [],
            },
        )

        self.task_a.refresh_from_db()

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertEqual(self.task_a.priority, Task.PRIORITY_HIGH)
        self.assertEqual(self.task_a.due_date, date(2026, 4, 12))

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        task_detail_response = self.client.get(reverse("task_detail", args=[self.task_a.pk]))
        task_list_response = self.client.get(reverse("task_list"))

        self.assertContains(board_detail_response, self.task_a.get_priority_display())
        self.assertContains(board_detail_response, "Vence 12 abr 2026")
        self.assertNotContains(board_detail_response, "Fecha límite: 12/04/2026")

        self.assertContains(task_detail_response, self.task_a.get_priority_display())
        self.assertContains(task_detail_response, "12/04/2026")

        self.assertContains(task_list_response, self.task_a.get_priority_display())
        self.assertContains(task_list_response, "Fecha límite: 12/04/2026")

    def test_task_update_can_clear_assignee(self):
        self.task_a.assignee = self.user_a
        self.task_a.save(update_fields=["assignee"])
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("task_update", args=[self.task_a.pk]),
            {
                "title": "Task A",
                "description": "Updated from the UI",
                "task_list": self.todo_a.pk,
                "assignee": "",
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [],
            },
        )

        self.task_a.refresh_from_db()

        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))
        self.assertIsNone(self.task_a.assignee)

    def test_task_update_keeps_selected_tags_bound_in_checkbox_list(self):
        tag_a = Tag.objects.create(board=self.board_a, name="Backend")
        tag_b = Tag.objects.create(board=self.board_a, name="API")
        self.task_a.tags.set([tag_a, tag_b])
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_update", args=[self.task_a.pk]))
        selected_values = {str(value) for value in response.context["form"]["tags"].value()}

        self.assertEqual(response.context["form"].fields["tags"].widget.__class__.__name__, "CheckboxSelectMultiple")
        self.assertEqual(response.context["form"].fields["tags"].widget.attrs["class"], "task-form-tag-checkbox")
        self.assertEqual(selected_values, {str(tag_a.pk), str(tag_b.pk)})
        self.assertContains(response, "(marca varias)")
        self.assertContains(response, 'task-form-bottom-side', html=False)
        self.assertContains(response, 'task-form-tag-options', html=False)
        self.assertContains(response, 'checked', html=False)

    def test_task_update_rejects_tag_from_another_board_same_owner(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_tag = Tag.objects.create(board=other_board, name="Later")
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("task_update", args=[self.task_a.pk]),
            {
                "title": "Task A",
                "description": "Updated from the UI",
                "task_list": self.todo_a.pk,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": "",
                "tags": [other_tag.pk],
            },
        )

        self.task_a.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn("tags", response.context["form"].errors)
        self.assertEqual(self.task_a.task_list, self.todo_a)
        self.assertFalse(self.task_a.tags.exists())

    def test_board_detail_shows_priority_badge_and_task_actions_for_visible_task(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_a.get_priority_display())
        self.assertContains(response, reverse("task_detail", args=[self.task_a.pk]))
        self.assertContains(response, reverse("task_update", args=[self.task_a.pk]))
        self.assertContains(response, reverse("task_delete", args=[self.task_a.pk]))

    def test_board_detail_shows_task_delete_action_for_hidden_task(self):
        hidden_task = self.task_a
        for index in range(5):
            hidden_task = Task.objects.create(
                title=f"Task hidden {index}",
                task_list=self.todo_a,
            )
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("task_delete", args=[hidden_task.pk]))

    def test_board_detail_shows_compact_due_date_metadata_for_hidden_task(self):
        for index in range(5):
            Task.objects.create(
                title=f"Task filler {index}",
                task_list=self.todo_a,
            )
        hidden_task = Task.objects.create(
            title="Task hidden with due date",
            task_list=self.todo_a,
            priority=Task.PRIORITY_HIGH,
            due_date=date(2026, 5, 18),
        )
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, hidden_task.title)
        self.assertContains(response, "Vence 18 may 2026")
        self.assertNotContains(response, "Fecha límite: 18/05/2026")

    def test_board_detail_and_task_detail_show_task_tags(self):
        tag_a = Tag.objects.create(board=self.board_a, name="Backend")
        self.task_a.tags.add(tag_a)
        self.client.force_login(self.user_a)

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        task_detail_response = self.client.get(reverse("task_detail", args=[self.task_a.pk]))

        self.assertContains(board_detail_response, "Etiquetas: Backend")
        self.assertContains(task_detail_response, "Backend")

    def test_board_detail_shows_compact_tag_management_zone(self):
        tag = Tag.objects.create(board=self.board_a, name="Backend")
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'board-panel-tags', html=False)
        self.assertContains(response, 'id="board-tags-title"', html=False)
        self.assertContains(response, "Etiquetas")
        self.assertContains(response, reverse("board_tag_create", args=[self.board_a.pk]))
        self.assertContains(response, reverse("board_tag_update", args=[self.board_a.pk, tag.pk]))
        self.assertContains(response, reverse("board_tag_delete", args=[self.board_a.pk, tag.pk]))
        self.assertContains(response, tag.name)

    def test_board_detail_shows_ver_mas_for_more_than_three_tags(self):
        for name in ["Backend", "API", "Urgente", "Bug"]:
            Tag.objects.create(board=self.board_a, name=name)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ver más")

    def test_board_detail_hides_ver_mas_for_three_tags_or_fewer(self):
        for name in ["Backend", "API", "Urgente"]:
            Tag.objects.create(board=self.board_a, name=name)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Ver más")

    def test_board_export_csv_requires_authentication(self):
        response = self.client.get(reverse("board_export_csv", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("board_export_csv", args=[self.board_a.pk]), response.url)

    def test_board_export_csv_rejects_foreign_board(self):
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_export_csv", args=[self.board_b.pk]))

        self.assertEqual(response.status_code, 404)

    def test_board_export_csv_returns_exact_header_and_task_rows_for_owned_board(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        backend = Tag.objects.create(board=self.board_a, name="Backend")
        api = Tag.objects.create(board=self.board_a, name="API")
        self.task_a.description = "Preparar backlog"
        self.task_a.priority = Task.PRIORITY_HIGH
        self.task_a.due_date = date(2026, 4, 15)
        self.task_a.assignee = self.user_a
        self.task_a.save(update_fields=["description", "priority", "due_date", "assignee"])
        self.task_a.tags.set([backend, api])
        later_task = Task.objects.create(
            title="Task B2",
            description="",
            task_list=doing,
            priority=Task.PRIORITY_LOW,
        )
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_export_csv", args=[self.board_a.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="board-{self.board_a.pk}-tasks.csv"',
        )

        rows = list(csv.reader(StringIO(response.content.decode("utf-8"))))

        self.assertEqual(
            rows[0],
            ["tablero", "lista", "titulo", "descripcion", "prioridad", "fecha_limite", "asignada_a", "etiquetas"],
        )
        self.assertEqual(
            rows[1],
            [
                self.board_a.name,
                self.todo_a.name,
                self.task_a.title,
                "Preparar backlog",
                "Alta",
                "2026-04-15",
                self.user_a.username,
                "API, Backend",
            ],
        )
        self.assertEqual(
            rows[2],
            [
                self.board_a.name,
                doing.name,
                later_task.title,
                "",
                "Baja",
                "",
                "",
                "",
            ],
        )
        self.assertEqual(len(rows), 3)

    def test_board_export_csv_for_empty_board_returns_header_only(self):
        empty_board = Board.objects.create(name="Board Empty", owner=self.user_a)
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("board_export_csv", args=[empty_board.pk]))

        self.assertEqual(response.status_code, 200)
        rows = list(csv.reader(StringIO(response.content.decode("utf-8"))))
        self.assertEqual(
            rows,
            [["tablero", "lista", "titulo", "descripcion", "prioridad", "fecha_limite", "asignada_a", "etiquetas"]],
        )

    def test_board_task_move_moves_task_to_another_list_and_redirects_to_detail(self):
        doing = TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_move", args=[self.board_a.pk, self.task_a.pk]),
            {
                f"move-{self.task_a.pk}-task_list": str(doing.pk),
            },
        )

        self.task_a.refresh_from_db()

        self.assertEqual(self.task_a.task_list, doing)
        self.assertRedirects(response, reverse("board_detail", args=[self.board_a.pk]))

        board_detail_response = self.client.get(reverse("board_detail", args=[self.board_a.pk]))
        self.assertContains(board_detail_response, self.task_a.title)
        self.assertContains(board_detail_response, doing.name)

    def test_board_task_move_rejects_task_list_from_another_board_same_owner(self):
        other_board = Board.objects.create(name="Board C", owner=self.user_a)
        other_task_list = TaskList.objects.create(board=other_board, name="Later", position=1)
        TaskList.objects.create(board=self.board_a, name="Doing", position=2)
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_move", args=[self.board_a.pk, self.task_a.pk]),
            {
                f"move-{self.task_a.pk}-task_list": str(other_task_list.pk),
            },
        )

        self.task_a.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.task_a.task_list, self.todo_a)
        self.assertContains(response, "Selecciona una lista válida.")

    def test_user_cannot_move_foreign_task_from_board_detail(self):
        self.client.force_login(self.user_a)

        response = self.client.post(
            reverse("board_task_move", args=[self.board_b.pk, self.task_b.pk]),
            {
                f"move-{self.task_b.pk}-task_list": str(self.todo_b.pk),
            },
        )

        self.assertEqual(response.status_code, 404)
        self.task_b.refresh_from_db()
        self.assertEqual(self.task_b.task_list, self.todo_b)

    def test_task_create_form_only_exposes_owned_task_lists(self):
        Tag.objects.create(board=self.board_a, name="Backend")
        self.client.force_login(self.user_a)

        response = self.client.get(reverse("task_create"))

        self.assertEqual(response.status_code, 200)
        task_list_field = response.context["form"].fields["task_list"]
        self.assertEqual(list(task_list_field.queryset), [self.todo_a])
        self.assertEqual(list(response.context["form"].fields["assignee"].queryset), [self.user_a])
        self.assertNotIn("tags", response.context["form"].fields)
        self.assertContains(response, "Las etiquetas se asignan cuando la tarea se crea desde un tablero concreto.")

    def test_task_create_with_owned_task_list_query_param_exposes_matching_board_tags(self):
        tag_a = Tag.objects.create(board=self.board_a, name="Backend")
        Tag.objects.create(board=self.board_b, name="Urgente")
        self.client.force_login(self.user_a)

        response = self.client.get(f'{reverse("task_create")}?task_list={self.todo_a.pk}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["board"], self.board_a)
        self.assertEqual(response.context["preselected_task_list"], self.todo_a)
        self.assertEqual(list(response.context["form"].fields["tags"].queryset), [tag_a])

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
