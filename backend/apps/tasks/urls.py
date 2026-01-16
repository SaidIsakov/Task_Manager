from apps.tasks.views import TaskViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, 'tasks')

app_name = 'tasks'

urlpatterns = [
    path('', include(router.urls))
]

