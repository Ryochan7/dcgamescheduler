from django.contrib import admin
from profile.models import UserProfile

class UserProfileAdmin (admin.ModelAdmin):
    pass

admin.site.register (UserProfile, UserProfileAdmin)

