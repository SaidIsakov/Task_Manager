import os
from celery import Celery
from celery.schedules import crontab


# Говорим Celery, где настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('task_manager')

# Загружаем настройки из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в apps/*/tasks.py
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-spam-every-1-minute': {
        'task': 'apps.tasks.tasks.send_message_overdue_tasks',
        'schedule': crontab(minute=0, hour=9)
    },
}
