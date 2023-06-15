from rest_framework import permissions

class IsOwner(permissions.BasePermission):
  
  def has_object_permission(self, request, view, obj):
    return bool(obj.id == request.user.id)