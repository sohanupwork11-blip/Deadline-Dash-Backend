from django.db.models import Count, Q
from rest_framework import serializers

from projects.models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(read_only=True)
    completed_task_count = serializers.IntegerField(read_only=True)
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            "id", "name", "description", "status", "start_date", "due_date",
            "task_count", "completed_task_count", "progress_percentage", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_progress_percentage(self, project):
        task_count = getattr(project, "task_count", 0)
        if task_count == 0:
            return 0
        completed_count = getattr(project, "completed_task_count", 0)
        return round(completed_count * 100 / task_count)


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.none())

    class Meta:
        model = Task
        fields = (
            "id", "project", "title", "description", "status", "priority",
            "due_date", "completed_at", "created_at", "updated_at",
        )
        read_only_fields = ("id", "completed_at", "created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["project"].queryset = Project.objects.filter(owner=request.user)