from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Task

class TaskViewSet(ModelViewSet):
  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя c новой задачей
    """
    serializer.save(created_by=self.request.user)

  def get_queryset(self):
    """ Показывает задачи, которые пренадлежат проектам только текущего пользователя """
    return Task.objects.filter(project__owner=self.request.user)
