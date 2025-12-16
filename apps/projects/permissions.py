from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from .models import ProjectMember, ProjectRole


def get_project_membership(user, project):
    """
    Возвращает ProjectMember или None
    """
    return ProjectMember.objects.filter(
        user=user,
        project=project,
        is_active=True
    ).first()


class IsProjectOwnerOrAdmin(BasePermission):
  def has_object_permission(self, request, view, obj):
    membership = get_project_membership(request.user, obj)
    if not membership:
      return False

    return membership.role in [
            ProjectRole.OWNER,
            ProjectRole.ADMIN
        ]


class IsMember(BasePermission):
  """ Участник """
  def has_object_permission(self, request, view, obj):
     return ProjectMember.objects.filter(
            user=request.user,
            project=obj,
            is_active=True
        ).exists()


class IsProjectOwner(BasePermission):
  """
  Только OWNER
  """

  def has_object_permission(self, request, view, obj):
    membership = get_project_membership(request.user, obj)

    if not membership:
        return False

    return membership.role == ProjectRole.OWNER
