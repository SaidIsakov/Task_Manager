from django.db import models
from apps.projects.models import Project
from django.conf import settings

class TaskStatus(models.TextChoices):
  NEW = 'new', 'New',
  IN_PROGRESS = 'in_progress', 'In_progress',
  DONE = 'done', 'Done'


class Task(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    related_name='tasks'
  )
  assignee = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='tasks'
  )
  status = models.CharField(
    max_length=20,
    choices=TaskStatus.choices,
    default = TaskStatus.NEW
  )

  created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='created_tasks'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.title

