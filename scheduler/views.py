# Create your views here.

import calendar
import datetime
from dateutil.relativedelta import relativedelta
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseBadRequest, Http404
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from timezones.utils import localtime_for_timezone, adjust_datetime_to_timezone
from scheduler.models import Game, Event, Attendance
from scheduler.forms import CalendarForm, GameSelectForm, EventRegisterForm, EventEditForm
from profile.models import UserProfile
from django.core.validators import MinValueValidator

@login_required
def event_edit (request, event_id):
    event_id = int (event_id)
    event = get_object_or_404 (Event, id = event_id)
    if request.method == "POST":
        form = EventEditForm (request.POST, timezone=request.user_profile.timezone, instance=event)
        if form.is_valid ():
#            event = form.save (commit = False)
            form.save ()
            """            print event.start
            print event.end
            print request.user_profile
            event.start = adjust_datetime_to_timezone (event.start, request.user_profile.timezone)
            event.end = adjust_datetime_to_timezone (event.end, request.user_profile.timezone)
            print event.start
            print event.end
            event.save ()
            """
            return redirect ("event_details", event.id)
        else:
            context = {
                "form": form,
                "event": event,
            }
            return direct_to_template (request, "edit_event.html", context)

    elif request.method == "GET":
        context = {
            "form": EventEditForm (timezone=request.user_profile.timezone, instance=event),
            "event": event,
        }
        return direct_to_template (request, "edit_event.html", context)

    return HttpResponseBadRequest ()

@login_required
def create_event (request):
    if request.method == "POST":
        stuff = request.POST.copy ()
        stuff["submitter"] = request.user
        print "BACON"
        form = EventRegisterForm (request.POST)
        if form.is_valid ():
            event = form.save (commit = False)
            event.submitter = request.user
            """
            event.start = adjust_datetime_to_timezone (event.start, request.user_profile)
            event.end = adjust_datetime_to_timezone (event.end, request.user_profile)
            """
            event.save ()
            return redirect ("event_details", event.id)
        else:
            print 'JLKLJFSDKL'
            context = {
                "form": form,
            }
            return direct_to_template (request, "create_event.html", context)

    elif request.method == "GET":
        context = {
            "form": EventRegisterForm (),
        }
        return direct_to_template (request, "create_event.html", context)

    return HttpResponseBadRequest()

def search_index (request):
    if request.method == "POST":
        form = CalendarForm (request.POST)
        if form.is_valid ():
            return redirect ("date_index", form.cleaned_data["month"], form.cleaned_data["year"])
            
    return HttpResponseBadRequest ()

def index (request, month=None, year=None):
    profile = None
    if request.user.is_authenticated ():
#        profile = UserProfile.objects.get (user = request.user)
        profile = request.user_profile

    month = datetime.datetime.now ().month if not month else int (month)
    year = datetime.datetime.now ().year if not year else int (year)
    current_date = datetime.datetime.now ()
    lookup_date = datetime.datetime (year, month, 01)
    next_month = lookup_date + relativedelta (months = +1)
    prev_month = lookup_date + relativedelta (months = -1)

    calendar_days = calendar.Calendar (calendar.SUNDAY).itermonthdates (year, month)
#    print calendar_days
    """
    search_date = datetime.datetime (year, 01, 01)
    month_list = []
    month_list.append (search_date)
    while search_date.month != 12:
        search_date = search_date + relativedelta (months = +1)
        month_list.append (search_date)
    """

    game_id = game_form = events = None
    # Form has been used to filter calendar events by game id.
    # game_id variable will be populated and used to filter events
    if "game_id" in request.GET:
        game_form = GameSelectForm (Game.objects.all ().order_by ("name"), request.GET)
        if not game_form.is_valid ():
            game_form = GameSelectForm (Game.objects.all ().order_by ("name"))
        # Reset filter was chosen. Remove game_id from user session
        elif game_form.cleaned_data["game_id"] == GameSelectForm.RESET_FILTER:
            if "game_id" in request.session:
                del request.session["game_id"]
        # Add game_id to sesesion
        else:
            game = get_object_or_404 (Game, id = game_form.cleaned_data["game_id"])
            request.session["game_id"] = game.id
            game_id = game.id
    # Retrieve game_id from current session
    elif "game_id" in request.session:
        try:
            game = Game.objects.get (id = request.session["game_id"])
            game_form = GameSelectForm (Game.objects.all ().order_by ("name"), {"game_id": game.id})
            game_id = game.id
        # Delete game_id from session if game does not exist
        except Game.DoesNotExist:
            del request.session["game_id"]
    # Neither the form nor session have a filter
    else:
        game_form = GameSelectForm (Game.objects.all ().order_by ("name"))


    games = Game.objects.all ()
    events = Event.objects.filter (start__gte = lookup_date, end__lt = next_month)
    if game_id:
        events = events.filter (game__id = game_id)

    event_list = list (events)
    print event_list
    date_list = []

    for date in calendar_days:
        cal_day = {}
        cal_day["date"] = date
        cal_day["items"] = []
        remove_indexes = []
        for i, event in enumerate (event_list[:]):
            # Handle events in current date
            if event.start.date () == date and event.end.date () >= date:
                cal_day["items"].append (event)
            # Handle events that have already passed
            elif event.start.date () < date and event.end.date () < date:
                remove_indexes.append (i)

        # Remove any passed events from list
        remove_indexes.reverse ()
        for i in remove_indexes:
            del event_list[i]

        date_list.append (cal_day)

    print event_list
    context = {
        "games": games,
        "events": events,
        "lookup_date": lookup_date,
        "next_month": next_month,
        "prev_month": prev_month,
        "calendar_days": calendar_days,
        "date_list": date_list,
        "search_form": CalendarForm ({"month": month, "year": year}),
        "game_form": game_form,
        "current_date": current_date,
        "profile": profile,
    }
    return direct_to_template (request, "calendar.html", context)


def mark_event_attendance (request, event_id, mark="attending"):
    event_id = int (event_id)

    if request.method == "POST":
        event = get_object_or_404 (Event, id = event_id)
        attend = Attendance.objects.filter (user = request.user, event = event).exists ()
        if mark == "attend":
            if attend:
                request.user.message_set.create (message = "You are already marked as attending")
            else:
                Attendance.objects.create (user = request.user, event=event)
                request.user.message_set.create (message = "You are now marked as attending")

            return redirect ("event_details", event_id)

        elif mark == "unattend":
            if not attend:
                request.user.message_set.create (message = "You were not attending")
            else:
                record = Attendance.objects.filter ()
                record.delete ()
                request.user.message_set.create (message = "You are no longer attending")

            return redirect ("event_details", event_id)

    return HttpResponseBadRequest ()


def event_details (request, event_id):
    profile = None
    if request.user.is_authenticated ():
        profile = UserProfile.objects.get (user = request.user)

    """
    print profile
    print profile.timezone

    print adjust_datetime_to_timezone (datetime.datetime.now (), profile.timezone)
    print localtime_for_timezone (datetime.datetime.utcnow (), profile.timezone)
    """

    context = {
        "queryset" : Event.objects.all ().select_related (depth=1),
        "object_id" : event_id,
        "template_name" : "event_details.html",
        "template_object_name" : "event",
        "extra_context": {
            "is_attending": Attendance.objects.filter (user = request.user, event__id = event_id).exists () if request.user.is_authenticated () else False,
            "num_attendees": Attendance.objects.filter (event__id = event_id).count (),
            "attendees": User.objects.filter (attendance__in = Attendance.objects.filter (event__id = event_id)),
            "profile": profile,
        }
    }
    return object_detail (request, **context)


def game_details (request, game_id):
    context = {
        "queryset" : Game.objects.all ().select_related (depth=1),
        "object_id" : game_id,
        "template_name" : "game_details.html",
        "template_object_name" : "game",
        "extra_context": {
            "event_count": Event.objects.filter (game__id = game_id).count (),
        }
    }
    return object_detail (request, **context)


def events_for_game (request, game_id):
    game_id = int (game_id)
    game = get_object_or_404 (Game, id = game_id)
    event_list = Event.objects.filter (game = game).annotate (Count ("attendance")).order_by ("-start", "-id")
    
    context = {
        "queryset": event_list,
        "template_name": "events_for_game.html",
        "template_object_name": "event",
        "extra_context": {
            "game": game,
        }
    }

    return object_list (request, **context)

def game_list (request):
    context = {
        "queryset": Game.objects.all ().select_related (depth=1).annotate (Count ("event")),
        "template_name": "game_list.html",
        "template_object_name": "game",
    }
    return object_list (request, **context)

