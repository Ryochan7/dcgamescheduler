class UserProfileMiddleware (object):
    def process_request (self, request):
        if request.user.is_authenticated () and request.user.profiles.count () == 1:
            request.user_profile = request.user.profiles.all ()[0]

