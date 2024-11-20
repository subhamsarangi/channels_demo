from django.urls import reverse
from django.core.exceptions import PermissionDenied


class RestrictStaffToAdminMiddleware:
    """
    Middleware that restricts staff members from accessing the admin panel.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_url = reverse("admin:index")

    def __call__(self, request):
        if request.path.startswith(self.admin_url):
            if not request.user.is_authenticated:
                raise PermissionDenied("You must be logged in to access this page.")
            elif not request.user.is_staff:
                raise PermissionDenied(
                    "Access denied. You must be a staff member to access this page."
                )

        response = self.get_response(request)
        return response
