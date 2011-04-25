from django.contrib import admin
from scheduler.models import Game, Event, Attendance

class GameAdmin (admin.ModelAdmin):
    pass

class EventAdmin (admin.ModelAdmin):
    fields = ("title", "game", "submitter", "description", "start", "end")
    list_display = ("title", "game", "submitter", "start", "end")
    list_filter = ("start", "end")
    search_fields = ["title", "game__name"]
    ordering = ("title",)

class AttendanceAdmin (admin.ModelAdmin):
    pass

admin.site.register (Game, GameAdmin)
admin.site.register (Event, EventAdmin)
admin.site.register (Attendance, AttendanceAdmin)

