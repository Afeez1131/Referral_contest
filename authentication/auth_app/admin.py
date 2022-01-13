from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChageForm, CustomUserCreationForm
# Register your models here.
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChageForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'is_superuser', 'is_active')


admin.site.register(CustomUser, CustomUserAdmin)
