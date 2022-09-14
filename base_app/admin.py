from django.contrib import admin
from .models import Referral, Guest
from auth_app.models import BusinessOwner


# Register your models here.
class AdminRefer(admin.TabularInline):
    model = Referral
    max_num = 3
    extra = 0


class AdminGuest(admin.ModelAdmin):
    list_display = ["referral", "business_owner", "guest_name", "ip"]
    list_filter = ['business_owner', 'guest_name']


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
        "guest_count",
    ]
    list_filter = ['business_owner']
    search_fields = ['refer_name', 'phone_number']
    # inlines = [GuestAdmin]


admin.site.register(Guest, AdminGuest)
admin.site.register(Referral, ReferAdmin)
