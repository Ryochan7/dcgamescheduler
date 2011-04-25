from registration.forms import RegistrationForm
from timezones.forms import TimeZoneField

class CustomRegistrationForm (RegistrationForm):
    timezone = TimeZoneField ()

