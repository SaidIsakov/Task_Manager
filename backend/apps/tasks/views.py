from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from .permissions import CanCreateTask, CanUpdateTask, CanDeleteTask,IsTaskProjectMember
from django.db.models import Q
class TaskViewSet(ModelViewSet):
  serializer_class = TaskSerializer

  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя c новой задачей
    """
    serializer.save(created_by=self.request.user)

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
