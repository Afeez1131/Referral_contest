from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('retrieve-user/', views.RetrieveBusinessOwner.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('obtain-token/', views.ObtainToken.as_view(), name='obtain_token'),

    path('user/', views.ListBusinessOwners.as_view(), name='users'),
    path('user/<pk>/', views.ListBusinessOwners.as_view(), name='retrieve-user'),
    # path('user/<pk>/', views.RetrieveBusinessOwner.as_view(), name='retrieve-user'),

    path('create/', views.CreateBusinessOwner.as_view(), name='create_user'),
    # path('users/', views.RetrieveBusinessOwner.as_view(), name='users'),

    path('contest/', views.ListContests.as_view(), name='contests'),
    path('contest/<pk>/', views.RetrieveUpdateContest.as_view(), name='retrieve-contest'),
    # path('contest/<pk>/referral/', views.CreateContestReferral.as_view(), name='create_contest_referral'),

    path('referral/', views.ListReferral.as_view(), name='referrals'),
    # path('referral/create/', views.CreateReferral.as_view(), name='create_referral'),
    path('referral/<pk>/', views.RetrieveUpdateReferral.as_view(), name='referral'),
    path('referral/<pk>/vote/', views.GuestVoteReferral.as_view(), name='vote_referral'),

    # path('guest/create/', views.CreateGuest.as_view(), name='create_guest'),
    path('guest/', views.ListGuest.as_view(), name='guest'),
    path('guest/<pk>/', views.RetrieveUpdateGuest.as_view(), name='retrieve-guest'),
    # path('guest-vote/', views.GuestVote.as_view(), name='guest-vote'),
    # path('business-owner/', views.RetrieveBusinessOwner.as_view()),
]