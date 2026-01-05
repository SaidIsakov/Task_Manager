from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.projects.views import ProjectViewSet
from apps.tasks.views import TaskViewSet, IndexView
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', IndexView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('^social/', include('social_django.urls', namespace='social')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
]
