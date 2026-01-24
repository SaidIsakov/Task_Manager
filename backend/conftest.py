import pytest
from apps.users.models import User
from rest_framework.test import APIClient
from apps.projects.models import Project, ProjectMember, ProjectRole
from apps.tasks.models import Task


@pytest.fixture
def user():
  return User.objects.create()


@pytest.fixture
def auth_client(user):
  client = APIClient()
  client.force_login(user)

  return client


@pytest.fixture
def project(user):
  return Project.objects.create(owner=user, name="Test Project", description="This is Test")


@pytest.fixture
def project_member(project, user):
  project_member_user = ProjectMember.objects.create(user=user, project=project, role=ProjectRole.ADMIN)

  return project_member_user


@pytest.fixture
def create_user(db):
  def _create_user(username):
    return User.objects.create(username=username)
  return _create_user


@pytest.fixture
def add_member_to_project(db):
  def _add_member(user, project, role):
    return ProjectMember.objects.create(user=user, project=project, role=role)
  return _add_member
