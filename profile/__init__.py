from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from registration import signals
from registration.backends.default import DefaultBackend
from registration.models import RegistrationProfile


class CustomRegistrationBackend (DefaultBackend):

    def register(self, request, **kwargs):
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site, send_email=False)

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

