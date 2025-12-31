from rest_framework import serializers
from .models import Task
from apps.projects.models import Project, ProjectMember, ProjectRole

class TaskSerializer(serializers.ModelSerializer):
  created_by = serializers.PrimaryKeyRelatedField(read_only=True)


  class Meta:
    model = Task
    fields = ['id',
              'title',
              'description',
              'project',
              'assignee',
              'status',
              'created_by',
              'created_at',
              'updated_at'
              ]

  def validate(self,  data):
    self._validate_completed_task(data)

    request = self.context['request']
    user = request.user

    if self.instance is None:
      return data

    task = self.instance
    project = task.project

    try:
      membership = ProjectMember.objects.get(
        user=user,
        project=project,
        is_active=True
      )
    except ProjectMember.DoesNotExist:
      raise serializers.ValidationError(
        'Вы не участник проекта'
      )

    new_assignee = data.get('assignee', task.assignee)

    if new_assignee == task.assignee:
      return data

    if membership.role == ProjectRole.VIEWER:
      raise serializers.ValidationError(
        'VIEWER не может менять исполнителя'
      )

    if membership.role == ProjectRole.MEMBER:
      if new_assignee != user:
        raise serializers.ValidationError(
          'MEMBER может назначать исполнителем только себя'
        )
    try:
      assignee_membership = ProjectMember.objects.get(
        user=new_assignee,
        project=project,
        is_active=True
      )
    except ProjectMember.DoesNotExist:
      raise serializers.ValidationError(
        'Исполнитель не является участником проекта'
      )

    if assignee_membership.role == ProjectRole.VIEWER:
      raise serializers.ValidationError(
        'Нельзя назначить VIEWER исполнителем'
      )

    return data

  def _validate_completed_task(self, data):
    if data.get('status') == 'done' and not data.get('description'):
      raise serializers.ValidationError({
        'description': 'Завершённая задача должна иметь описание!'
      })
