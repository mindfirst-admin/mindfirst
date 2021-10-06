from django.urls import path
from . import views

app_name = "characters"

urlpatterns = [
    path("add-new-behaviour", views.add_new_behaviour, name="add_new_behaviour"),
    path("get-behaviors", views.get_behaviors, name="get_behaviors"),

    path("update-behaviour", views.update_behaviour, name="update_behaviour"),
    path("delete-behaviour", views.delete_behaviour, name="delete_behaviour"),

    path("select-behaviour", views.select_behavior, name="select_behavior"),

    path("change-aspiration-name", views.change_aspiration_name, name="change_aspiration_name"),

    path("go-to-habit", views.go_to_habit_design, name="go_to_habit_design"),
    path("design-good-habit", views.design_good_habit, name="design_good_habit"),
    path("design-bad-habit", views.design_bad_habit, name="design_bad_habit"),
    path("scale-habit", views.scale_habit, name="scale_habit"),

    path("record-habit", views.record_habit, name="record_habit"),

    path("update-beliefs", views.update_beliefs, name="update_beliefs"),

    path("get-chart-data", views.get_chart_data, name="get_chart_data"),
    path("get-weekly-chart-data", views.get_weekly_chart_data, name="get_weekly_chart_data"),
]
