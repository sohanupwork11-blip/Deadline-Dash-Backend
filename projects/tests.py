from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from projects.models import Project


class ProjectApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="a-secure-test-password")
        self.other_user = User.objects.create_user(username="other", password="a-secure-test-password")

    def test_project_creation_sets_owner_and_reports_progress(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/projects/", {"name": "Launch", "status": "active"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["progress_percentage"], 0)
        self.assertEqual(Project.objects.get().owner, self.user)

    def test_users_cannot_read_another_users_project(self):
        project = Project.objects.create(owner=self.other_user, name="Private")
        self.client.force_authenticate(self.user)

        response = self.client.get(f"/api/projects/{project.pk}/")

        self.assertEqual(response.status_code, 404)

    def test_completed_task_gets_completion_timestamp(self):
        project = Project.objects.create(owner=self.user, name="Launch")
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/api/tasks/",
            {"project": project.pk, "title": "Ship release", "status": "done"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data["completed_at"])