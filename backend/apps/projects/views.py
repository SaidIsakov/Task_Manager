from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .permissions import IsProjectOwnerOrAdmin, IsMember, IsProjectOwner
from django.db.models import Q


class ProjectViewSet(ModelViewSet):
  serializer_class = ProjectSerializer
  pagination_class = None
  def perform_create(self, serializer):
    """
    Автоматически связывает нашего пользователя с новым проектом
    """
    serializer.save(owner=self.request.user)

  def get_permissions(self):
    if self.action in ['update', 'partial_update']:
      return [IsProjectOwnerOrAdmin()]
    if self.action == 'destroy':
      return [IsProjectOwner()]
    return [IsMember()]

  def get_queryset(self):
    """ Проеты видит толко участник и владелец """
    user = self.request.user

    return Project.objects.filter(
      Q(owner=user) | Q(members__user=user, members__is_active=True)
    ).distinct()

