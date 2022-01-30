from django.conf import settings
from django.contrib.auth.hashers import check_password
from auth_app.models import BusinessOwner


class CustomUserBackend:
    def authenticate(self, request, phone_number=None, password=None):
        if phone_number and password:
            try:
                user = BusinessOwner.objects.get(phone_number=phone_number)
                if check_password(password, user.password):
                    if user.is_active:
                        return user
            except BusinessOwner.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return BusinessOwner.objects.get(pk=user_id)
        except BusinessOwner.DoesNotExist:
            return None
