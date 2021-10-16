from django.urls import path
from . import views

app_name = "template"

urlpatterns = [
    path("take-control-over-your-habits/week~<int:week_id>", views.take_control_over_your_habits,
         name="take_control_over_your_habits"),

    path("get-started/day/~<int:day_id>", views.day_, name="day"),

    path("mind-workshop/week~<int:week_id>", views.mind_workshop, name="mind_workshop"),
]
