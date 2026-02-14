from rest_framework import serializers
from .models import Project
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
  examples = [
   OpenApiExample(
    "Project Details",
    summary="Project Detail example",
    value = {
      "id": 14,
      "name": 'Create models',
      "description" : "Create Category model for project",
      "owner": 1,
      "created_at": "2007-11-12T00:00:00Z"
      }
    )
  ]
)
class ProjectSerializer(serializers.ModelSerializer):
  owner = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Project
    fields = ['id', 'name', 'description', 'owner', 'created_at']
