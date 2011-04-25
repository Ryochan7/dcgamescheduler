import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from registration.forms import RegistrationForm
from timezones.forms import TimeZoneField, LocalizedDateTimeField
from timezones.utils import localtime_for_timezone, adjust_datetime_to_timezone
from time import strftime
from scheduler.fields import JqSplitDateTimeField
from scheduler.widgets import JqSplitDateTimeWidget
from scheduler.models import Game, Event

class CalendarForm (forms.Form):
    MONTH_CHOICES = (
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    )

    YEAR_CHOICES = [(i, str (i)) for i in range (2010, 2050)]
    month = forms.ChoiceField (choices=MONTH_CHOICES, widget=forms.Select ())
    year = forms.ChoiceField (choices=YEAR_CHOICES, widget=forms.Select ())


class GameSelectForm (forms.Form):
    RESET_FILTER = "0"
    INITIAL_CHOICES = (RESET_FILTER, "-----")

    def __init__ (self, games, *args, **kwargs):
        super (forms.Form, self).__init__ (*args, **kwargs)
        self.fields["game_id"].choices = [self.INITIAL_CHOICES]
        self.fields["game_id"].choices.extend ([(game.id, game.name) for game in games])

    game_id = forms.ChoiceField (label=u"Game:", widget=forms.Select ())


class EventRegisterForm (forms.ModelForm):

    start = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}))
    end = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}))

    def __init__ (self, *args, **kwargs):
        self.timezone = None
        if "timezone" in kwargs:
            self.timezone = kwargs["timezone"]
            del kwargs["timezone"]

        super (EventRegisterForm, self).__init__ (*args, **kwargs)

    def clean (self):
        super (EventRegisterForm, self).clean ()
        start = end = None
        if "start" in self.cleaned_data:
            start = self.cleaned_data["start"]

        if "end" in self.cleaned_data:
            end = self.cleaned_data["end"]

        if start and end and start >= end:
            raise forms.ValidationError ("Start date can not be after the ending date")

        return self.cleaned_data

    def clean_start (self):
        date = self.cleaned_data["start"]
        if date < datetime.datetime.now ():
            raise forms.ValidationError ("Starting event date can not be in the past")

        print "IN CLEAN START"

        if self.timezone:
            print date
            date = adjust_datetime_to_timezone (date, self.timezone)
            print date
        return date


    def clean_end (self):
        date = self.cleaned_data["end"]
        if date < datetime.datetime.now ():
            raise forms.ValidationError ("Ending event date can not be in the past")

        print "IN CLEAN END"

        if self.timezone:
            print date
            date = adjust_datetime_to_timezone (date, self.timezone)
            print date
        return date


    class Meta (object):
        model = Event
        fields = ("title", "start", "end", "game", "description")

    class Media (object):
       css = {
          "all": ("css/event_form.css", "css/smoothness/jquery-ui-1.8.9.custom.css",),
       }
       js = (
          "js/jquery-1.5.min.js",
          "js/jquery-ui-1.8.9.custom.min.js",
          "js/jqsplitdatetime.js",
       )



class EventEditForm (EventRegisterForm):

    def __init__ (self, *args, **kwargs):
        super (EventEditForm, self).__init__ (*args, **kwargs)

        if "instance" in kwargs and self.timezone:
            instance = kwargs["instance"]
            print kwargs
            print args
            if not "initial" in kwargs:
                kwargs["initial"] = {}

            kwargs["initial"].update ({"start": localtime_for_timezone (instance.start, self.timezone)})
            kwargs["initial"].update ({"end": localtime_for_timezone (instance.start, self.timezone)})


    def clean_start (self):
        date = self.cleaned_data["start"]
        if self.timezone:
            print "IN CLEAN START EDIT"
            print date
            date = adjust_datetime_to_timezone (date, self.timezone)
            print date

        return date


    def clean_end (self):
        date = self.cleaned_data["end"]
        if self.timezone:
            print "IN CLEAN END EDIT"
            print date
            date = adjust_datetime_to_timezone (date, self.timezone)
            print date

        return date


class CustomRegistrationForm (RegistrationForm):
    timezone = TimeZoneField ()


