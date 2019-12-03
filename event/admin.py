from django.contrib import admin

from .models import Profile, PublicEvent, PrivateEvent

# Register your models here.

admin.site.register(Profile)
admin.site.register(PublicEvent)
admin.site.register(PrivateEvent)