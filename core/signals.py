from django.contrib.auth.models import User
from core.models import WatchList, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def create_watchlist(sender, instance, created, **kwargs):
    if created:
        WatchList.objects.create(profile=instance)