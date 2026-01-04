from celery import shared_task


@shared_task
def send_email(user_email):
  print("Письмо отправлено")
