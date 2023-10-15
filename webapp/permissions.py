from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def role_required(*role_names):
    """Requires user to have at least one of the specified roles."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user  # Get the user object from the request
            if not any(role in user.role for role in role_names):
                messages.error(request,
                               'You do not have permission to access this page. Contact your Technical Administrator '
                               'for further assistance.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('dashboard')))
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

