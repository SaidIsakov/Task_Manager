from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .permissions import IsProjectOwner

class ProjectViewSet(ModelViewSet):
  serializer_class = ProjectSerializer
  permission_classes = [IsAuthenticated, IsProjectOwner]

  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя с новым проектом
    """
    serializer.save(owner=self.request.user)

  def get_queryset(self):
    """ Показывает проекты только текущего пользователя """
    return Project.objects.filter(owner=self.request.user)

