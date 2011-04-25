import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator

# Create your models here.

class Game (models.Model):
    name = models.CharField (max_length=50, unique=True)
    full_image = models.ImageField (upload_to="gameimages", max_length=255, height_field="full_image_height", width_field="full_image_width")
    thumbnail = models.ImageField (upload_to="gamethumbs", max_length=255, height_field="thumbnail_height", width_field="thumbnail_width")#, editable=False)#, blank=True)
    full_image_height = models.SmallIntegerField (editable=False)
    full_image_width = models.SmallIntegerField (editable=False)
    thumbnail_height = models.SmallIntegerField (editable=False)
    thumbnail_width = models.SmallIntegerField (editable=False)
    #description = models.TextField (validators=[MinLengthValidator (10), MaxLengthValidator (2000)])


    def __unicode__ (self):
        return self.name

    def __repr__ (self):
        return self.name

    @models.permalink
    def get_absolute_url (self):
        return ("game_details", (), {"game_id": self.id})

#    def save (self, *args, **kwargs):
#        super (Game, self).save (*args, **kwargs)


class Event (models.Model):
    title = models.CharField (max_length=50)
    start = models.DateTimeField ()
    end = models.DateTimeField ()
    submitter = models.ForeignKey (User)
    game = models.ForeignKey (Game)
    description = models.TextField (validators=[MinLengthValidator (10), MaxLengthValidator (2000)])

    def __unicode__ (self):
        return u"%s - %s" % (self.title, self.game.name)

    def __repr__ (self):
        return self.title

    @models.permalink
    def get_absolute_url (self):
        return ("event_details", (), {"event_id": self.id})


class Attendance (models.Model):
    user = models.ForeignKey (User)
    event = models.ForeignKey (Event)
    date_linked = models.DateTimeField (default=datetime.datetime.now)

    class Meta (object):
        unique_together =  ("user", "event",)

    def __unicode__ (self):
        return u"%s - %s" % (self.user.username, self.event.title)

    def __repr__ (self):
        return u"%s - %s" % (self.user.username, self.event.title)


