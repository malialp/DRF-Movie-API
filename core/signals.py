from django.contrib.auth.models import User
from core.models import WatchList
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_watchlist(sender, instance, created, **kwargs):
    if created:
        WatchList.objects.create(user=instance)