from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered
from timezones.fields import TimeZoneField
from timezones.utils import localtime_for_timezone, adjust_datetime_to_timezone

# Create your models here.

class UserProfile (models.Model):
    user = models.ForeignKey (User, related_name="profiles")
    timezone = TimeZoneField ()

    def __unicode__ (self):
        return self.user.username

    @classmethod
    def create_from_registration (cls, sender, user, request, **kwargs):
        # Will get here when registration.views.register sends the
        # user_registered signal. Form class set to CustomRegistrationForm
        # for view so assumed timezone will be included with request.
        print request.POST
        print request.POST["timezone"]
        UserProfile.objects.create (user = user, timezone = request.POST["timezone"])


user_registered.connect (UserProfile.create_from_registration)
