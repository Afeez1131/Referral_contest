from django.urls import path
from .views import HomePageView, ProfilePage
urlpatterns = [ 
    path('', HomePageView.as_view(), name='home'),
    path('profile/', ProfilePage.as_view(), name='profile'),
]