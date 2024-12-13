from django.contrib import admin
from django.utils.decorators import method_decorator

from .utils import restrict_ip


# provision for a module to add trusted ip address
class CustomAdminSite(admin.AdminSite):
    @method_decorator(restrict_ip())
    def each_context(self, request):
        return super().each_context(request)


custom_admin_site = CustomAdminSite(name="custom_admin")

from apps.myauth.models import User
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "is_active", "is_admin")
    readonly_fields = ("last_login",)
    exclude = ("password",)


custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group)

from apps.api.models import Profile

custom_admin_site.register(Profile)


from apps.chat.models import ChatRoom, ChatRoomMembership

custom_admin_site.register(ChatRoom)

custom_admin_site.register(ChatRoomMembership)
