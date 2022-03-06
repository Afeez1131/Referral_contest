from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Contest

from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "full_name", "is_active", "is_staff", "shortcode")
    fieldsets = (
        (None, {"fields": ("username", "full_name")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
        ("Personal", {"fields": ("business_name", "phone_number")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "username",
                    "full_name",
                    "business_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contest)
