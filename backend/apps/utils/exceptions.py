# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status

# def custom_exception_handler(exc, context):
#   response = exception_handler(exc, context)

#   if response is not None:
#     custom_reponse_data = {
#       'error': {
#         'code': 'api_error',
#         'message': 'Произошла ошибка при обработке запроса.',
#         'details': response.data
#       }
#     }
#     response.data = custom_reponse_data
#   else:
#     custom_reponse_data = {
#       'error': {
#         'code': 'internal_error',
#         'message': 'Внутренняя ошибка сервера.',
#         'details': {}
#       }
#     }
#     response = Response(
#         custom_reponse_data,
#         status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
#       )
#   return response
