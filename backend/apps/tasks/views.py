from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from .permissions import CanCreateTask, CanUpdateTask, CanDeleteTask,IsTaskProjectMember
from .filters import TaskFilter
from .tasks import send_email_assignee
from django.views.generic import TemplateView
from apps.projects.models import ProjectMember, ProjectRole, Project


class IndexView(TemplateView):
  template_name = 'index.html'


class TaskViewSet(ModelViewSet):
  serializer_class = TaskSerializer
  filterset_class = TaskFilter

  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя c новой задачей
    """
    task = serializer.save(created_by=self.request.user)
    text = f"""
    {task.assignee.username} у вас новая задача!
    Детали:
      id: {task.id}
      title: {task.title}
      description: {task.description}
      status: {task.status}
      project: {task.project}
      deadline: {task.deadline}
      """
    send_email_assignee(task.assignee.telegram_id, text)

  def get_queryset(self):
    user = self.request.user

    full_access_projects = ProjectMember.objects.filter(
        user=user,
        role__in=[ProjectRole.ADMIN, ProjectRole.VIEWER, ProjectRole.OWNER]
    ).values_list('project_id', flat=True)

    owned_projects = Project.objects.filter(owner=user).values_list('id', flat=True)

    all_full_access_project_ids = list(full_access_projects) + list(owned_projects)

    tasks = Task.objects.none()

    if all_full_access_project_ids:
        tasks |= Task.objects.filter(project_id__in=all_full_access_project_ids)

    tasks |= Task.objects.filter(assignee=user)

    return tasks.distinct()

  def get_permissions(self):
    if self.action in ['create']:
      return [CanCreateTask()]
    if self.action in ['update', 'partial_update']:
      return [CanUpdateTask()]
    if self.action in ['destroy']:
      return [CanDeleteTask()]
    return [IsTaskProjectMember()]
