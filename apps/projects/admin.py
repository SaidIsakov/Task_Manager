from django.contrib import admin
from .models import Project, ProjectMember

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
  list_display = ['name', 'description', 'created_at']
  readonly_fields = ['created_at']


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
  list_display = ['user', 'project', 'role',
                  'invited_by', 'joined_at', 'is_active']
