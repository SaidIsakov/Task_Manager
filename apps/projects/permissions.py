from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsProjectOwner(BasePermission):
  pass
  # """
  #   Разрешает доступ только владельцу проекта.
  #   SAFE_METHODS (GET, HEAD, OPTIONS) тоже проверяются, но можно разрешить только владельцу.
  #   """
  # def get_object_permission(self, request, view, obj):
  #   return obj.owner == request.user
