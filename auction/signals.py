from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item, Auction


@receiver(post_save, sender=Item)
def create_Auction(sender, instance=None, created=False, **kwargs):
  if created:
    Auction.objects.create(item=instance)