from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from datetime import date

class AuctionPermission(BasePermission):
  def has_permission(self, request, view):
    if request.method == 'GET':
      return True
    
    if not request.user.is_authenticated:
      return False
    
    if request.method == 'PUT':
      instance = view.get_object()
      if instance.item.owner == request.user:
        raise PermissionDenied("You can not bid on your own item.")
      if instance.deadline_date < date.today():
        raise PermissionDenied("This auction has expired.")
      if instance.current_bid_owner == request.user:
        raise PermissionDenied("You already have the highest bid on this item.")
      return True

    if request.method == 'DELETE':
      instance = view.get_object()
      return instance.item.owner == request.user

    return False
  
class IsOwnerOrReadOnly(BasePermission):
  def has_object_permission(self, request, view, obj):
    
    if request.method in SAFE_METHODS:
      return True
    
    return obj.owner == request.user
      
  