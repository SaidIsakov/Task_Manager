import pytest
from apps.tasks.models import Task
from rest_framework import status
from apps.users.models import User
from apps.projects.models import ProjectMember, ProjectRole
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_task_create(project, auth_client, user, project_member):
  """
    Создание задачи
  """

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
def test_task_list(user, auth_client, project, project_member, task_factory):
  """
    Вывод списока задач
  """

  url = '/api/tasks/'

  task_factory(title="Test task 2", description="Test task Desc 2", project=project, assignee=user, status="new", created_by=user)

  response = auth_client.get(url)
  assert response.status_code == status.HTTP_200_OK
  results = response.data['results']
  print(results)
  assert len(results) == 1
  assert results[0]['title'] == "Test task 2" and results[0]['description'] == "Test task Desc 2"


@pytest.mark.django_db
def test_project_owner_can_see_all_tasks_in_project(user, project, project_member, auth_client,
                                                    create_user, add_member_to_project, task_factory):
  '''
    Владелец проекта видит все задачи в проекте, даже если они назначены другим пользователям.
  '''

  url = '/api/tasks/'

  other_user = create_user("Other_user")

  add_member_to_project(other_user, project, ProjectRole.MEMBER)

  task_factory(title="USER_TASK", description="Test task Desc USER", project=project, assignee=other_user, status="new", created_by=other_user)

  task_factory(title="Test task other_user", description="Test task Desc other_user", project=project, assignee=other_user, status="new", created_by=other_user)

  #! Запрос делает другой user(owner)
  response = auth_client.get(url)
  result = response.data['results']
  assert len(result) == 2
  assert result[0]["title"] == "USER_TASK"
  assert result[1]["title"] == "Test task other_user"


@pytest.mark.django_db
def test_project_member_sees_only_own_tasks(user, project, create_user, add_member_to_project,
                                            create_api_client, task_factory):
  '''
    Участник проекта может видеть только свои задачи
  '''

  url = '/api/tasks/'

  #! Создаю пользователей
  user1 = create_user("Other_user1")
  user2 = create_user("Other_user2")

  #! Присваиваю пользователям роль "Участник"
  add_member_to_project(user1, project, ProjectRole.MEMBER)
  add_member_to_project(user2, project, ProjectRole.MEMBER)

  #! Создал задачу для пользователя 1
  task_factory(title="USER1_TASK", description="Test task Desc USER", project=project, assignee=user1, status="new", created_by=user)

  #! Создал задачу для пользователя 2
  task_factory(title="USER2_TASK", description="Test task Desc other_user", project=project, assignee=user2, status="new", created_by=user)

  #! Логиню пользователя
  client = create_api_client(user1)
  response = client.get(url, format="json")
  result = response.data['results']

  assert response.status_code == status.HTTP_200_OK
  assert len(result) == 1
  print(result)
  assert result[0]["title"] == "USER1_TASK"


@pytest.mark.django_db
def test_admin_sees_all_tasks_in_project(project, create_user, add_member_to_project, create_api_client, task_factory):
  """
    Админ проекта видит все задачи
  """
  url = '/api/tasks/'

  admin_user = create_user('admin_user')
  member1 = create_user('member1')
  member2 = create_user('member2')

  #! Назначаю роли
  add_member_to_project(admin_user, project, ProjectRole.ADMIN)
  add_member_to_project(member1, project, ProjectRole.MEMBER)
  add_member_to_project(member2, project, ProjectRole.MEMBER)


   #! Создал задачу для пользователя 1
  task_factory(title="member1", description="Test task Desc member1", project=project, assignee=member1, status="new", created_by=admin_user)

  #! Создал задачу для пользователя 2
  task_factory(title="member2", description="Test task Desc member2", project=project, assignee=member2, status="new", created_by=admin_user)

  client = create_api_client(admin_user)
  response = client.get(url, format="json")
  results = response.data['results']

  assert response.status_code == status.HTTP_200_OK
  assert len(results) == 2
  titles = {task['title'] for task in results}
  assert titles == {"member1", "member2"}


@pytest.mark.django_db
def test_viewer_sees_all_tasks_in_project(user, project, create_user, add_member_to_project,
                                          create_api_client, task_factory):
  """
    Viewer может видеть все задачи
  """

  url = '/api/tasks/'

  #! Создаем пользователей
  viewer_user = create_user('viewer_user')
  member1 = create_user('member1')
  member2 = create_user('member2')

  #! Назначаю роли
  add_member_to_project(viewer_user, project, ProjectRole.VIEWER)
  add_member_to_project(member1, project, ProjectRole.MEMBER)
  add_member_to_project(member2, project, ProjectRole.MEMBER)

   #! Создал задачу для пользователя 1
  task_factory(title="member1", description="Test task Desc member1", project=project, assignee=member1, status="new", created_by=user)

  #! Создал задачу для пользователя 2
  task_factory(title="member2", description="Test task Desc member2", project=project, assignee=member2, status="new", created_by=user)

  client = create_api_client(viewer_user)
  response = client.get(url, format="json")
  results = response.data['results']

  assert response.status_code == status.HTTP_200_OK
  assert len(results) == 2
  titles = {task['title'] for task in results}
  assert titles == {"member1", "member2"}


@pytest.mark.django_db
def test_member_cannot_delete_task(project, user, create_user, add_member_to_project, create_api_client, task_factory):
  """
    MEMBER не может удалить задачу
  """


  #! Создаем пользователя
  member = create_user('member')

  #! Присваиваю ему роль MEMBER
  add_member_to_project(member, project, ProjectRole.MEMBER)

  #! Создаем задачу где наш пользователь(member) исполнитель
  task = task_factory(title="task_member1", description="Test task Desc member1", project=project, assignee=member, status="new", created_by=user)

  client = create_api_client(member)
  response = client.delete(f'/api/tasks/{task.id}/')

  assert response.status_code == status.HTTP_403_FORBIDDEN
  assert Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_viewer_cannot_delete_task(project, user, create_user, add_member_to_project, create_api_client, task_factory):
  """
    VIEWER не может удалить задачу
  """

  #! Создаем пользователя
  viewer = create_user('viewer')
  member = create_user('member')

  #! Добавляем участников в проект
  add_member_to_project(viewer, project, ProjectRole.VIEWER)
  add_member_to_project(member, project, ProjectRole.MEMBER)

  #! Создаем задачу где наш пользователь(member) исполнитель
  task = task_factory(title="task_member1", description="Test task Desc member1", project=project, assignee=member, status="new", created_by=user)

  client = create_api_client(viewer)
  response = client.delete(f'/api/tasks/{task.id}/')

  assert response.status_code == status.HTTP_403_FORBIDDEN
  assert Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_admin_can_delete_task(project, user, create_user, add_member_to_project, create_api_client, task_factory):
  """
    ADMIN может удалять задачи
  """

  #! Создаю пользователей
  admin_user = create_user('admin_user')
  member = create_user('member')

  #!  Добавляем участников в проект
  add_member_to_project(admin_user, project, ProjectRole.ADMIN)
  add_member_to_project(member, project, ProjectRole.MEMBER)

  #! Создаём задачу, назначенную на другого пользователя
  task = task_factory(title="member_task",
        description="...",
        project=project,
        assignee=member,
        status="new",
        created_by=user)

  client = create_api_client(admin_user)
  response = client.delete(f'/api/tasks/{task.id}/')

  assert response.status_code == status.HTTP_204_NO_CONTENT
  assert not Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_owner_can_delete_task(project, user, create_user, add_member_to_project, create_api_client, task_factory):
  """
    OWNER может удалять задачи
  """

  #! Создаю пользователей
  owner = create_user('owner_user')
  member = create_user('member')

  #!  Добавляем участников в проект
  add_member_to_project(owner, project, ProjectRole.OWNER)
  add_member_to_project(member, project, ProjectRole.MEMBER)

  #! Создаём задачу, назначенную на другого пользователя
  task = task_factory(title="member_task",
        description="...",
        project=project,
        assignee=member,
        status="new",
        created_by=user)

  client = create_api_client(owner)
  response = client.delete(f'/api/tasks/{task.id}/')

  assert response.status_code == status.HTTP_204_NO_CONTENT
  assert not Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_admin_can_update_task(user, project, create_user, create_api_client, task_factory,
                               add_member_to_project):
  """
  ADMIN может редактировать задач
  """
   #! Создаем пользователей
  admin = create_user('admin')
  member = create_user('member')

  add_member_to_project(admin, project, ProjectRole.ADMIN)
  add_member_to_project(member, project, ProjectRole.MEMBER)

  #! Создаю задачи
  task = task_factory(project=project, assignee=member, title='Old title', created_by=user)

  #! Авторизация как админ
  client = create_api_client(admin)

  response = client.patch(
    f'/api/tasks/{task.id}/',
    {"title" : "Updated by Admin"},
    format="json"
  )

  assert response.status_code == status.HTTP_200_OK
  assert response.data["title"] == "Updated by Admin"

@pytest.mark.django_db
def test_owner_can_update_task(user, project, create_user, create_api_client, task_factory,
                               add_member_to_project):
  """
  OWNER может редактировать задач
  """
   #! Создаем пользователей
  owner = create_user('owner')
  member = create_user('member')

  add_member_to_project(owner, project, ProjectRole.OWNER)
  add_member_to_project(member, project, ProjectRole.MEMBER)

  #! Создаю задачи
  task = task_factory(project=project, assignee=member, title='Old title', created_by=user)

  #! Авторизация как owner
  client = create_api_client(owner)

  response = client.patch(
    f'/api/tasks/{task.id}/',
    {"title" : "Updated by Owner"},
    format="json"
  )

  assert response.status_code == status.HTTP_200_OK
  assert response.data["title"] == "Updated by Owner"


@pytest.mark.django_db
def test_member_can_update_own_task(user, project, create_user, create_api_client, task_factory,
                               add_member_to_project):
  """
  MEMBER может редактировать только свою задачу
  """
   #! Создаем пользователей
  member1 = create_user('member1')

  add_member_to_project(member1, project, ProjectRole.MEMBER)

  #! Создаю задачи
  task = task_factory(project=project, assignee=member1, title='Old title', created_by=user)

  #! Авторизация как member
  client = create_api_client(member1)

  response = client.patch(
    f'/api/tasks/{task.id}/',
    {"title" : "Updated by Member1"},
    format="json"
  )

  assert response.status_code == status.HTTP_200_OK
  assert response.data["title"] == "Updated by Member1"


@pytest.mark.django_db
def test_member_cannot_update_other_task(user, project, create_user, create_api_client, task_factory,
                                         add_member_to_project):
  """
  MEMBER не может редактировать чужие задачи --> HTTP_404_NOT_FOUND
  """
   #! Создаем пользователей
  member1 = create_user('member1')
  member2 = create_user('member2')

  add_member_to_project(member1, project, ProjectRole.MEMBER)
  add_member_to_project(member2, project, ProjectRole.MEMBER)

  #! Создаю задачи
  task = task_factory(project=project, assignee=member2, title='Old title', created_by=user)

  #! Авторизация как member
  client = create_api_client(member1)

  response = client.patch(
    f'/api/tasks/{task.id}/',
    {"title" : "Updated by Member1"},
    format="json"
  )

  assert response.status_code == status.HTTP_404_NOT_FOUND
  task.refresh_from_db()
  assert task.title == 'Old title'

@pytest.mark.django_db
def test_viewer_cannot_update_other_task(user, project, create_user, create_api_client, task_factory,
                                         add_member_to_project):
  """
  VIEWER не может редактировать чужие задачи --> HTTP_403_FORBIDDEN
  """
   #! Создаем пользователей
  member = create_user('member1')
  viewer = create_user('viewer')

  add_member_to_project(member, project, ProjectRole.MEMBER)
  add_member_to_project(viewer, project, ProjectRole.VIEWER)

  #! Создаю задачи
  task = task_factory(project=project, assignee=member, title='Old title', created_by=user)

  #! Авторизация как viewer
  client = create_api_client(viewer)

  response = client.patch(
    f'/api/tasks/{task.id}/',
    {"title" : "Updated by Viewer"},
    format="json"
  )

  assert response.status_code == status.HTTP_403_FORBIDDEN
  task.refresh_from_db()
  assert task.title == 'Old title'



@pytest.mark.django_db
def test_viewer_cannot_update_own_task(user, project, create_user, create_api_client, task_factory,
                                         add_member_to_project):
  """
  VIEWER не может редактировать свою задачу --> HTTP_403_FORBIDDEN
  """
   #! Создаем пользователей
  viewer = create_user('viewer')

  add_member_to_project(viewer, project, ProjectRole.VIEWER)

  #! Создаю задачи
  task = task_factory(project=project, assignee=viewer, title='Old title', created_by=user)

  #! Авторизация как viewer
  client = create_api_client(viewer)

  response = client.patch(
    f'/api/tasks/{task.id}/',
    {"title" : "Updated by Viewer"},
    format="json"
  )

  assert response.status_code == status.HTTP_403_FORBIDDEN
