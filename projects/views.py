from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Project, Task
from projects.permissions import IsProjectOwner
from projects.serializers import ProjectSerializer, TaskSerializer


class DashboardSummaryView(APIView):
    def get(self, request):
        today = timezone.localdate()
        week_end = today + timedelta(days=7)
        project_counts = Project.objects.filter(owner=request.user).aggregate(
            total=Count("id"),
            active=Count("id", filter=Q(status=Project.Status.ACTIVE)),
            completed=Count("id", filter=Q(status=Project.Status.COMPLETED)),
        )
        task_counts = Task.objects.filter(project__owner=request.user).aggregate(
            total=Count("id"),
            open=Count("id", filter=~Q(status=Task.Status.DONE)),
            overdue=Count(
                "id",
                filter=Q(due_date__lt=today) & ~Q(status=Task.Status.DONE),
            ),
            due_this_week=Count(
                "id",
                filter=Q(due_date__gte=today, due_date__lte=week_end)
                & ~Q(status=Task.Status.DONE),
            ),
        )
        return Response({"projects": project_counts, "tasks": task_counts})


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["due_date", "created_at", "status", "name"]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).annotate(
            task_count=Count("tasks", distinct=True),
            completed_task_count=Count("tasks", filter=Q(tasks__status=Task.Status.DONE), distinct=True),
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsProjectOwner]
    filterset_fields = ["project", "status", "priority"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at", "priority", "status"]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user).select_related("project")

    def perform_create(self, serializer):
        task = serializer.save()
        if task.status == Task.Status.DONE:
            task.completed_at = timezone.now()
            task.save(update_fields=["completed_at", "updated_at"])

    def perform_update(self, serializer):
        task = serializer.save()
        if task.status == Task.Status.DONE and task.completed_at is None:
            task.completed_at = timezone.now()
            task.save(update_fields=["completed_at", "updated_at"])
        elif task.status != Task.Status.DONE and task.completed_at is not None:
            task.completed_at = None
            task.save(update_fields=["completed_at", "updated_at"])