from .models import Item, Auction
from .serializers import ItemSerializer, AuctionSerializer, ItemUpdateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .permissions import AuctionPermission, IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet

class ItemView(ModelViewSet):
  queryset = Item.objects.all()
  serializer_class = ItemSerializer
  permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
  
  def get_serializer_class(self):
    if self.action == 'update':
      return ItemUpdateSerializer
    return super().get_serializer_class()
  
  
class AuctionView(ModelViewSet):
  queryset = Auction.objects.all()
  serializer_class = AuctionSerializer
  permission_classes = [AuctionPermission]
  
  def get(self, request, *args, **kwargs):
    instance = self.get_object()

    if instance.deadline_date < date.today():
      if instance.current_bid_owner: # if not null, it means someone bid on it
        # Change the owner of the item to the last current_bid_owner
        instance.item.owner = instance.current_bid_owner
        instance.item.save()
      instance.is_auction_open = False
      instance.save()

    serializer = self.get_serializer(instance)
    return Response(serializer.data)