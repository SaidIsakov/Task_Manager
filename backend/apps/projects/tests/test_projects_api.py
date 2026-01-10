import pytest
from rest_framework import status
from apps.projects.models import Project


class TestProjectAPI():
  @pytest.mark.django_db
  def test_project_create(self, auth_client, user):
    """
      test для создания проекта
    """

    url = '/api/projects/'
    data = {
      "name": "Test_Case",
      "description": "This is Test",
    }

    response = auth_client.post(url, data, format="json")
    assert response.status_code  == status.HTTP_201_CREATED
    assert response.data["name"] == "Test_Case"

    project = Project.objects.get(name="Test_Case")
    assert project.description == "This is Test"
    assert project.owner == user


  @pytest.mark.django_db
  def test_project_list(self, auth_client, user):
    """
      test для получения проектов
    """

    Project.objects.create(owner=user, name="Test", description="Desc")

    url = '/api/projects/'
    response = auth_client.get(url)

    assert len(response.data) == 1
    assert response.data[0]["name"] == "Test"
    assert response.data[0]['description'] == "Desc"
    assert response.data[0]["owner"] == user.id

