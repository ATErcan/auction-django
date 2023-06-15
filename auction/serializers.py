from rest_framework import serializers
from .models import Item, Auction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class UserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = ('username')

class AuctionSerializer(serializers.ModelSerializer):
  
  current_bid_owner = serializers.ReadOnlyField(source='current_bid_owner.username')
  
  class Meta:
    model = Auction
    fields = (
      'item',
      'current_bid',
      'current_bid_owner',
      'listed_date',
      'deadline_date',
      'last_updated',
      'is_auction_open'      
    )
    extra_kwargs = {
      'item': {'required': False}
    }
    
  def update(self, instance, validated_data):
    requested_bid = validated_data.get('current_bid')
    base_price = instance.item.base_price
    current_bid = instance.current_bid

    if current_bid is None:
      if requested_bid is not None and requested_bid > base_price:
        instance.current_bid = requested_bid
        instance.current_bid_owner = self.context['request'].user
        instance.save()
        return instance
    else:
      if requested_bid is not None and requested_bid > current_bid:
        instance.current_bid = requested_bid
        instance.current_bid_owner = self.context['request'].user
        instance.save()
        return instance

    raise serializers.ValidationError("You can not bid lower than or equal to base price or previous bid.")
    
class ItemSerializer(serializers.ModelSerializer):
  auction = AuctionSerializer(read_only=True)
  
  class Meta:
    model = Item
    fields = (
      'id',
      'name',
      'base_price',
      'image',
      'owner',
      'auction',
    )
    extra_kwargs = {
      'owner': {'required': False}
    }
  
  def create(self, validated_data):
    user = self.context['request'].user
    validated_data['owner'] = user
    return super().create(validated_data)
  

class ItemUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = ('name', 'image')

  def update(self, instance, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.image = validated_data.get('image', instance.image)
    instance.save()
    return instance