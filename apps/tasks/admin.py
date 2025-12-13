from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
  list_display = ['title', 'description', 'project',
                  'assignee', 'status', 'created_by']
  readonly_fields = ['created_at', 'updated_at']
