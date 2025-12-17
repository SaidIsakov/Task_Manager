from rest_framework import serializers
from .models import Task
from apps.projects.models import Project, ProjectMember, ProjectRole

class TaskSerializer(serializers.ModelSerializer):
  assignee = serializers.CharField()
  created_by = serializers.CharField()

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

  def validate(self, attrs):
    request = self.context['request']
    user = request.user

    if self.instance is None:
      return attrs

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

    new_assignee = attrs.get('assignee', task.assignee)

    if new_assignee == task.assignee:
      return attrs

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

    return attrs


