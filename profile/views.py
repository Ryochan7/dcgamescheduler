# Create your views here.

from django.views.generic.simple import direct_to_template

def edit_timezone (request):
#    form = TimeZoneForm ()
    
    context = {
#        "form": form,
    }
    return direct_to_template (request, "edit_timezone.html", context)


def edit_profile (request):
    #form = ProfileForm ()
#    if request.method == "POST":
#        form = ProfileForm (request.POST)
#        if form.is_valid ():
#            form.save ()
#            return redirect ()
#        else:
#    elif request.method == "GET":
#        form = ProfileForm ()
#        context = {
#            "form": form,
#        }
        return direct_to_template (request, "edit_timezone.html", context)

#    return HttpBadRequestResponse ()    
