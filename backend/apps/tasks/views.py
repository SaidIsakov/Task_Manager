from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from .permissions import CanCreateTask, CanUpdateTask, CanDeleteTask,IsTaskProjectMember
from django.db.models import Q
from .filters import TaskFilter
from .tasks import send_email_assignee
from django.views.generic import TemplateView

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
      """
    send_email_assignee(task.assignee.telegram_id, text)

  def get_queryset(self):
    """ Показывает задачи только владельцам проекта и кому принадлежит задача """
    user = self.request.user
    return Task.objects.filter(
    Q(project__owner=user) | Q(assignee=user)
    )

  def get_permissions(self):
    if self.action in ['create']:
      return [CanCreateTask()]
    if self.action in ['update', 'partial_update']:
      return [CanUpdateTask()]
    if self.action in ['destroy']:
      return [CanDeleteTask()]
    return [IsTaskProjectMember()]
