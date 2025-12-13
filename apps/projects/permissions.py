from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProjectOwner(BasePermission):
  """
    Разрешает доступ только владельцу проекта.
    SAFE_METHODS (GET, HEAD, OPTIONS) тоже проверяются, но можно разрешить только владельцу.
    """
  def get_object_permission(self, request, view, obj):
    return obj.owner == request.user
