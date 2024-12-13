from django.core.exceptions import PermissionDenied
from functools import wraps


def restrict_ip():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            client_ip = request.META.get("REMOTE_ADDR")
            # allowed_ips
            # if client_ip not in allowed_ips:
            # raise PermissionDenied("Access denied.")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
