from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Task

class TaskViewSet(ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя c новой задачей
    """
    serializer.save(created_by=self.request.user)

