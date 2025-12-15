from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Project(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  owner = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='owned_projects'
  )
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.name


class ProjectRole(models.TextChoices):
  OWNER = 'OWNER', 'Owner',
  ADMIN = 'ADMIN', 'Admin',
  MEMBER = 'MEMEBER', 'Member',
  VIEWER = 'VIEWER', 'Viewer'


class ProjectMember(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='project_memberships'
  )
  project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    related_name='members'
  )
  role = models.CharField(
    max_length=10,
    choices=ProjectRole.choices,
    default=ProjectRole.MEMBER
  )
  invited_by = models.ForeignKey(
    User,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='invited_members'
  )
  joined_at = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)

  class Meta:
    unique_together = ('user', 'project')
