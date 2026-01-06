from celery import shared_task
import requests
from django.conf import settings


@shared_task
def send_email_assignee(telegram_id, text):
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
