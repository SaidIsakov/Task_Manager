import pytest
from apps.tasks.models import Task
from rest_framework import status


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
