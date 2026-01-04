import os
from celery import Celery

# Говорим Celery, где настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('task_manager')

# Загружаем настройки из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в apps/*/tasks.py
app.autodiscover_tasks()
