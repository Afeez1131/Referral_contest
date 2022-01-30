from django.contrib import admin
from .models import Referral, Guest
from auth_app.models import BusinessOwner

# Register your models here.
class AdminRefer(admin.TabularInline):
    model = Referral
    max_num = 3
    extra = 0


class AdminGuest(admin.ModelAdmin):
    list_display = ["referral", "business", "guest_name", "ip", "guest_count"]


class GuestAdmin(admin.TabularInline):
    model = Guest
    max_num = 3
    extra = 1


class ReferAdmin(admin.ModelAdmin):
    list_display = [
        "refer_name",
        "phone_number",
        "ref_shortcode",
        "business_owner",
    ]
    inlines = [GuestAdmin]


admin.site.register(Guest, AdminGuest)
admin.site.register(Referral, ReferAdmin)
