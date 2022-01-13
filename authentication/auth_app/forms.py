from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        models = get_user_model()
        fields = ('username', 'email', )


class CustomUserChageForm(UserChangeForm):
    class Meta:
        models = get_user_model()
        fields = ('username', 'email', )
