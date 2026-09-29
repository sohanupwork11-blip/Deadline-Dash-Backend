from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = getattr(obj, "project", obj)
        return project.owner_id == request.user.id