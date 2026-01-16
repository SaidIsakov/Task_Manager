from apps.projects.views import ProjectViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

app_name = 'projects'

urlpatterns = [
    path('', include(router.urls))
]

