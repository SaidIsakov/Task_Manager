from celery import shared_task


@shared_task
def send_email(user_email):
  print(f"Письмо отправлено на {user_email}")
