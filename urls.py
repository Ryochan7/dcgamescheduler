from django.conf.urls.defaults import *
from django.conf import settings
from registration.views import register
from profile.forms import CustomRegistrationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^dcgamescheduler/', include('dcgamescheduler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url (r"^$", "scheduler.views.index", name="index"),
    url (r"^(?P<month>\d+)/(?P<year>\d+)/$", "scheduler.views.index", name="date_index"),
    url (r"^datesearch/$", "scheduler.views.search_index", name="search_index"),

    url (r"^game/(?P<game_id>\d+)/$", "scheduler.views.game_details", name="game_details"),
    url (r"^games/$", "scheduler.views.game_list", name="game_list"),
    url (r"^events/(?P<game_id>\d+)/$", "scheduler.views.events_for_game", name="events_for_game"),

    url (r"^event/(?P<event_id>\d+)/$", "scheduler.views.event_details", name="event_details"),
    url (r"^event/attend/(?P<event_id>\d+)/$", "scheduler.views.mark_event_attendance", {"mark": "attend"}, name="event_attend"),
    url (r"^event/remove/(?P<event_id>\d+)/$", "scheduler.views.mark_event_attendance", {"mark": "unattend"}, name="event_unattend"),
    url (r"^event/create/$", "scheduler.views.create_event", name="event_create"),
    url (r"^event/edit/(?P<event_id>\d+)/$", "scheduler.views.event_edit", name="event_edit"),

   url(r'^accounts/register/$', register, {"backend": "profile.CustomRegistrationBackend", "form_class": CustomRegistrationForm}, name='registration_register'),

    (r'^accounts/', include('registration.urls')),

)

if settings.DEBUG:
    urlpatterns += patterns ('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

