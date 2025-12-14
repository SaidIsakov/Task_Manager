from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .permissions import IsProjectOwner
from django.db.models import Q


class ProjectViewSet(ModelViewSet):
  serializer_class = ProjectSerializer
  permission_classes = [IsAuthenticated, IsProjectOwner]

  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя с новым проектом
    """
    serializer.save(owner=self.request.user)

  def get_queryset(self):
    """ Проеты видит толко участник и владелец """
    user = self.request.user

    return Project.objects.filter(
      Q(owner=user) | Q(members=user)
    ).distinct()

