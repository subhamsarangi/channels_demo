from django.core.exceptions import PermissionDenied
from functools import wraps


def restrict_ip(allowed_ip):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            client_ip = request.META.get("REMOTE_ADDR")
            if client_ip != allowed_ip:
                raise PermissionDenied("Access denied.")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
