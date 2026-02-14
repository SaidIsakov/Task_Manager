from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from .permissions import CanCreateTask, CanUpdateTask, CanDeleteTask,IsTaskProjectMember
from .filters import TaskFilter
from .tasks import send_email_assignee
from django.views.generic import TemplateView
from apps.projects.models import ProjectMember, ProjectRole, Project
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse


class IndexView(TemplateView):
  template_name = 'index.html'


@extend_schema_view(
    list=extend_schema(
        tags=['tasks'],
        summary="Список задач",
        description="""
        Возвращает задачи, доступные пользователю в зависимости от его роли в проектах:

        - OWNER/ADMIN/VIEWER: все задачи во всех проектах, где он участник
        - MEMBER: только задачи, назначенные на него
        """,
        responses={
            200: TaskSerializer(many=True),
        }
    ),
    create=extend_schema(
        tags=['tasks'],
        summary="Создать задачу",
        description="""
        Создаёт новую задачу в указанном проекте.

        Требования:
        - Пользователь должен быть участником проекта (любая роль)
        - Поле `assignee` должно быть участником того же проекта
        """,
        request=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: OpenApiResponse(description="Неверные данные"),
            403: OpenApiResponse(description="Нет доступа к проекту"),
        }
    ),
    retrieve=extend_schema(
        tags=['tasks'],
        summary="Получить задачу",
        description="""
        Возвращает детали одной задачи.
        """,
        responses={
            200: TaskSerializer,
            404: OpenApiResponse(description="Задача не найдена или нет доступа"),
        }
    ),
    update=extend_schema(
        tags=['tasks'],
        summary="Обновить задачу полностью",
        description="""
        Обновляет все поля задачи.

        Права:
        - OWNER/ADMIN: могут обновлять любые задачи в проекте
        - MEMBER: может обновлять только свои задачи
        - VIEWER: запрещено
        """,
        request=TaskSerializer,
        responses={
            200: TaskSerializer,
            403: OpenApiResponse(description="Нет прав на редактирование"),
            404: OpenApiResponse(description="Задача не найдена"),
        }
    ),
    partial_update=extend_schema(
        tags=['tasks'],
        summary="Частично обновить задачу",
        description="""
        Обновляет только указанные поля.

        Права такие же, как у полного обновления.
        """,
        request=TaskSerializer,
        responses={
            200: TaskSerializer,
            403: OpenApiResponse(description="Нет прав на редактирование"),
            404: OpenApiResponse(description="Задача не найдена"),
        }
    ),
    destroy=extend_schema(
        tags=['tasks'],
        summary="Удалить задачу",
        description="""
        Удаляет задачу из проекта.

        Права:
        - OWNER/ADMIN: могут удалять любые задачи
        - MEMBER/VIEWER: запрещено
        """,
        responses={
            204: OpenApiResponse(description="Задача удалена"),
            403: OpenApiResponse(description="Нет прав на удаление"),
            404: OpenApiResponse(description="Задача не найдена"),
        }
    )
)
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
    user = self.request.user.id

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


