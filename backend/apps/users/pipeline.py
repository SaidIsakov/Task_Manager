def save_telegram_id(strategy, details, response, user=None, *args, **kwargs):
  """ Сохраняет telegram_id """
  if user and 'id' in response:
    user.telegram_id = response['id']
    user.save()
