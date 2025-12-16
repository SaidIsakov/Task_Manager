from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.projects.models import ProjectMember, ProjectRole


def get_project_membership(user, project):
  return ProjectMember.objects.filter(
    user=user,
    project=project,
    is_active=True
  ).first()

class IsTaskProjectMember(BasePermission):
  def has_object_permission(self, request, view, obj):
    membership = get_project_membership(
      request.user,
      obj.project
    )
    return membership is not None


class CanCreateTask(BasePermission):
  """
  Создавать задачу могут все, кроме VIEWER
  """
  def has_permission(self, request, view):
    project_id = request.data.get('project')
    if not project_id:
      False

    membership = get_project_membership(
      request.user,
      project_id=project_id,
      is_active=True
    ).first()

    if not membership:
      return False

    return membership.role != ProjectRole.VIEWER


class CanUpdateTask(BasePermission):
    """
    OWNER / ADMIN — любую
    MEMBER — только свою
    """

    def has_object_permission(self, request, view, obj):
        membership = get_project_membership(
            request.user,
            obj.project
        )

        if not membership:
            return False

        if membership.role in [ProjectRole.OWNER, ProjectRole.ADMIN]:
            return True

        if membership.role == ProjectRole.MEMBER:
            return obj.assignee == request.user

        return False


class CanDeleteTask(BasePermission):
  """
  Только Owner или Admin
  """
  def has_object_permission(self, request, view, obj):
    membership = get_project_membership(
       request.user,
       obj.project
     )
    if not membership:
      return False
    return membership.role in [
      ProjectRole.OWNER,
      ProjectRole.ADMIN
    ]
