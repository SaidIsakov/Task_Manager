from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.tasks.views import TaskViewSet, IndexView
from apps.projects.urls import router as project_router
from apps.tasks.urls import router as tasks_router

router = DefaultRouter()

router.registry.extend(project_router.registry)
router.registry.extend(tasks_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('api/', include(router.urls)),
    path('auth/', include('social_django.urls', namespace='social')),
    re_path('^social/', include('social_django.urls', namespace='social')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
]
