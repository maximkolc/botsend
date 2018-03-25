from django.utils.timezone import now
from facebot.models import Profile
from django.utils.deprecation import MiddlewareMixin

class SetLastVisitMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated():
            # Update last visit time after request finished processing.
            p = Profile.objects.get(user=request.user)
            p.last_visit=now()
            p.save()
        return response 