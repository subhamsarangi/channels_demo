from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "is_active", "is_admin")
    readonly_fields = ("last_login",)
    exclude = ("password",)


admin.site.register(User, UserAdmin)
