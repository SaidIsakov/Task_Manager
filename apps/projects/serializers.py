from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
  owner = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Project
    fields = ['name', 'description', 'owner', 'members', 'created_at']
