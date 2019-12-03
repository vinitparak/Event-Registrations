from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class PublicEvent(models.Model):

    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    no_of_attendees = models.IntegerField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='eventimages/', default='default.jpg')


class PrivateEvent(models.Model):

    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    title = models.TextField()
    description = models.TextField()
    invitees = models.ManyToManyField(User, related_name='invitees')
    date = models.DateTimeField()
    image = models.ImageField(upload_to='eventimages/', default='default.jpg')


class RegisteredEvents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.TextField()

    class Meta:
        unique_together = (("user", "event"), )
