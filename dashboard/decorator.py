from functools import wraps
from django.shortcuts import redirect

from .utils import USER_TYPE_DEVELOPER, USER_TYPE_ADMIN, USER_TYPE_STAFF


def dashboard_access_required(user_types=()):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_type in user_types:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('login')

        return _wrapped_view

    return decorator


def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type in [
            USER_TYPE_DEVELOPER,
            USER_TYPE_ADMIN,
            USER_TYPE_STAFF,
        ]:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return _wrapped_view
