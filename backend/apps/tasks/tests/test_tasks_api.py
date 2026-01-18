import pytest
from apps.tasks.models import Task
from rest_framework import status
from apps.users.models import User
from apps.projects.models import ProjectMember, ProjectRole
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_task_create(project, auth_client, user, project_member):
  url = '/api/tasks/'


  data = {
    "title": "Test task",
    "description": "Test task Desc",
    "project": project.id,
    "assignee": user.id,
    "status": "new",
  }
  response = auth_client.post(url, data, format="json")
  print(response.data)
  assert response.status_code == status.HTTP_201_CREATED
  assert response.data["title"] == "Test task"
  assert response.data["description"] == "Test task Desc"


@pytest.mark.django_db
def test_task_list(user, auth_client, project, project_member):
  url = '/api/tasks/'
  Task.objects.create(title="Test task 2", description="Test task Desc 2", project=project, assignee=user, status="new", created_by=user)

  response = auth_client.get(url)
  assert response.status_code == status.HTTP_200_OK
  results = response.data['results']
  print(results)
  assert len(results) == 1
  assert results[0]['title'] == "Test task 2" and results[0]['description'] == "Test task Desc 2"


@pytest.mark.django_db
def test_project_owner_can_see_all_tasks_in_project(user, project, project_member, auth_client):
  '''
  Владелец проекта видит все задачи в проекте, даже если они назначены другим пользователям.
  '''

  url = '/api/tasks/'

  other_user = User.objects.create(username="Other_user")

  ProjectMember.objects.create(user=other_user, project=project, role=ProjectRole.MEMBER)

  Task.objects.create(title="USER_TASK", description="Test task Desc USER", project=project, assignee=other_user, status="new", created_by=other_user)

  Task.objects.create(title="Test task other_user", description="Test task Desc other_user", project=project, assignee=other_user, status="new", created_by=other_user)

  response = auth_client.get(url)
  result = response.data['results']
  assert len(result) == 2
  assert result[0]["title"] == "USER_TASK"
  assert result[1]["title"] == "Test task other_user"


@pytest.mark.django_db
def test_project_member_sees_only_own_tasks(user, project):
  '''
    Участник проекта может видеть только свои задачи
  '''

  url = '/api/tasks/'
  client = APIClient()

  #! Создаю пользователей
  user1 = User.objects.create(username="Other_user1")
  user2 = User.objects.create(username="Other_user2")

  #! Присваиваю пользователям роль "Участник"
  ProjectMember.objects.create(user=user1, project=project, role=ProjectRole.MEMBER)
  ProjectMember.objects.create(user=user2, project=project, role=ProjectRole.MEMBER)

  #! Создал задачу для пользователя 1
  Task.objects.create(title="USER1_TASK", description="Test task Desc USER", project=project, assignee=user1, status="new", created_by=user)

  #! Создал задачу для пользователя 2
  Task.objects.create(title="USER2_TASK", description="Test task Desc other_user", project=project, assignee=user2, status="new", created_by=user)

  #! Логиню пользователя
  client.force_login(user1)
  response = client.get(url, format="json")
  result = response.data['results']

  assert response.status_code == status.HTTP_200_OK
  assert len(result) == 1
  assert result[0]["title"] == "OTHER_USER1_TASK"
