import pytest
from apps.users.models import User
from rest_framework.test import APIClient

@pytest.fixture
def user():
  return User.objects.create()


@pytest.fixture
def auth_client(user):
  client = APIClient()
  client.force_login(user)

  return client
