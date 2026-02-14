from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .permissions import IsProjectOwnerOrAdmin, IsMember, IsProjectOwner
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from textwrap import dedent
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse



@extend_schema_view(
    list=extend_schema(
        tags=['projects'],
        summary="Список проектов",
        description="""
        Возвращает все проекты, где пользователь является владельцем или участником (любой роли).
        """,
        responses={
            200: ProjectSerializer(many=True),
        }
    ),
    create=extend_schema(
        tags=['projects'],
        summary="Создать проект",
        description="""
        Создаёт новый проект.
        """,
        request=ProjectSerializer,
        responses={
            201: ProjectSerializer,
        }
    ),
    retrieve=extend_schema(
        tags=['projects'],
        summary="Получить проект",
        description="""
        Возвращает детали одного проекта.
        """,
        responses={
            200: ProjectSerializer,
            404: OpenApiResponse(description="проект не найден или нет доступа"),
        }
    ),
    update=extend_schema(
        tags=['projects'],
        summary="Обновить проект полностью",
        description="""
        Обновляет все поля проекта.

        Права:
        - OWNER/ADMIN: могут обновлять проект
        - MEMBER: запрещено
        - VIEWER: запрещено
        """,
        request=ProjectSerializer,
        responses={
            200: ProjectSerializer,
            403: OpenApiResponse(description="Нет прав на редактирование"),
            404: OpenApiResponse(description="проект не найден"),
        }
    ),
    partial_update=extend_schema(
        tags=['projects'],
        summary="Частично обновить проект",
        description="""
        Обновляет только указанные поля.

        Права такие же, как у полного обновления.
        """,
        request=ProjectSerializer,
        responses={
            200: ProjectSerializer,
            403: OpenApiResponse(description="Нет прав на редактирование"),
            404: OpenApiResponse(description="Задача не найдена"),
        }
    ),
    destroy=extend_schema(
        tags=['projects'],
        summary="Удалить проект",
        description="""
        Удаляет проект.

        Права:
        - OWNER: может удалять проект
        - MEMBER/VIEWER/ADMIN: запрещено
        """,
        responses={
            204: OpenApiResponse(description="проект удален"),
            403: OpenApiResponse(description="Нет прав на удаление"),
            404: OpenApiResponse(description="Задача не найдена"),
        }
    )
)
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
      Q(owner=user) | Q(members__user=user)
    ).distinct()

