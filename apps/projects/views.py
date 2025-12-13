from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Project

class ProjectViewSet(ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя с новым проектом
    """
    serializer.save(owner=self.request.user)

