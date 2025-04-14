from django.http import HttpResponse
from functools import wraps
from django.contrib.auth.mixins import LoginRequiredMixin


def logged_in_user_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return HttpResponse("You are not authenticated!", status=403)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
