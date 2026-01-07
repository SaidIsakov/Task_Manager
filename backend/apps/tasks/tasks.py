from celery import shared_task
import requests
from django.conf import settings
from django.utils import timezone
from .models import Task
from apps.users.models import User

@shared_task
def send_email_assignee(telegram_id, text):
  """
    После создания задачи отправляет исполнителю сообщение в телеграм
  """
  bot_token = settings.TELEGRAM_BOT_TOKEN


  url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
  data = {
    'chat_id': telegram_id,
    'text': text
  }
  try:
    requests.post(url, data=data)
    print('Письмо отаравлено в Telegram!')
  except:
    print('Ошибка отправки сообщения в телеграм')

@shared_task
def send_message_overdue_tasks():
  """
    Найти всех пользователей с просроченными задачами
    и отправить каждому персональное уведомление
  """
  bot_token = settings.TELEGRAM_BOT_TOKEN
  url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

  for user in User.objects.filter(telegram_id__isnull=False):
    overdue_tasks = Task.objects.filter(
      assignee=user,
      status="new",
      deadline__lt=timezone.now()
    )

    if overdue_tasks.exists():
      text = f"{overdue_tasks.count()} задач просрочено. Хотите перенести дедлайн, назначить другому или закрыть?"
      data = {
        "chat_id": user.telegram_id,
        "text": text
      }

      try:
        requests.post(url, data=data)
        print(f'Уведомление отправлено пользователю {user.id} (телеграм: {user.telegram_id})')
      except Exception as e:
        print(f'Ошибка отправки пользователю {user.id}: {e}')

