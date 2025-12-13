from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = ['title',
              'description',
              'project',
              'assignee',
              'status',
              'created_by',
              'created_at',
              'updated_at'
              ]
