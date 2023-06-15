from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Item(models.Model):
  name = models.CharField(max_length=200)
  base_price = models.BigIntegerField()
  image = models.ImageField(upload_to="pictures", default="no_image.png")
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
  
  def __str__(self):
    return self.name 

class Auction(models.Model):
  def seven_day_hence():
    return date.today() + timedelta(days=7)
    
  item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
  current_bid = models.BigIntegerField(null=True, blank=True)
  current_bid_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  listed_date = models.DateField(auto_now_add=True)
  deadline_date = models.DateField(default=seven_day_hence, blank=True)
  last_updated = models.DateField(auto_now=True)
  is_auction_open = models.BooleanField(default=True, blank=True)
