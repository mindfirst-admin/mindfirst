from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("membership/reserve-your-spot/", views.reserve_membership_spot, name="reserve_membership_spot"),

    path("5-day-challenge", views.reserve_fd_challenge_spot, name="reserve_fd_challenge_spot"),

    path("members-area/sign-in/", views.sign_in_to_members_area, name="sign_in_to_members_area"),

    path("forgot-password/", views.user_forgot_password, name="user_forgot_password"),

    path("logout/", views.logout, name="logout"),
]

