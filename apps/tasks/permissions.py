from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAssigneeOrProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (просмотр) всем, у кого есть доступ к объекту через get_queryset
        if request.method in SAFE_METHODS:
            return True

        return obj.assignee == request.user or obj.project.owner == request.user
