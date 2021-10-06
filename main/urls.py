from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("members-area/", views.members_area, name="members_area"),

    path("vision-gallery/", views.vision_gallery, name="vision_gallery"),
    path("vision-gallery/edit_aspirations/", views.edit_aspirations, name="edit_aspirations"),
    path("vision-gallery/edit_values/", views.edit_values, name="edit_values"),
    path("vision-gallery/processing_video/", views.processing_video, name="processing_video"),
    path("vision-gallery/watch_video/", views.watch_video, name="watch_video"),

    path("behaviour-mapping/", views.behaviour_mapping, name="behaviour_mapping"),
    path("habit-design/", views.habit_design, name="habit_design"),

    path("habit-reporting/", views.habit_reporting, name="habit_reporting"),
    path("bad-habit-reporting/", views.bad_habit_reporting, name="bad_habit_reporting"),
    path("habit-summary/", views.habit_summary, name="habit_summary"),
    path("bad-habit-summary/", views.bad_habit_summary, name="bad_habit_sumary"),

    path("limiting-beliefs/", views.limiting_beliefs, name="limiting_beliefs"),


    path("take-control-over-your-habits/week~<int:week>", views.take_control, name="take_control"),
    path("get-started/day/~<int:day>", views.day_, name="day"),
    path("5-day-challenge/day/~<int:day>", views.five_day, name="five_day"),
    path("mind-workshop/week~<int:week>", views.mind_workshop, name="mind_workshop"),

    path("products/", views.products, name="products"),
    path("blog/", views.blog, name="blog"),

    path("login/", views.login, name="login"),
    path("sign-up/", views.sign_up, name="sign_up"),

    path("terms-and-conditions/", views.terms_and_conditions, name="terms_and_conditions"),

    path("add-payment/", views.add_payment, name="add_payment"),
    path("payment-successful/", views.payment_successful, name="payment_success"),
    path("payment-unsuccessful/", views.payment_unsuccessful, name="payment_failed"),

    path("forgot-password/", views.forgot_password_show, name="forgot_password"),

    path("logout/", views.logout_user, name="logout"),
]
