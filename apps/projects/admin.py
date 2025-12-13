from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
  list_display = ['name', 'description', 'owner', 'created_at']
  readonly_fields = ['created_at']
  filter_horizontal = ['members']
