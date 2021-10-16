from django.urls import path
from . import views, forms

app_name = 'behaviours'

urlpatterns = [
    path("", views.behaviour_mapping, name="behaviour_mapping"),

    path("habit-reporting/<str:orientation>/", views.habit_reporting, name="habit_reporting"),

    path("habit-design/<int:behaviour_id>/", views.habit_design, name="habit_design"),

    path("habit-summary/<str:orientation>/", views.habit_summary, name="habit_summary"),

    # forms
    path("change-aspiration-name", forms.change_aspiration_name, name="change_aspiration_name"),

    path("save-mapping", forms.select_behavior, name="select_behavior"),

    path("delete-behaviour", forms.delete_behaviour, name="delete_behaviour"),

    path("add-behaviour", forms.add_behaviour, name="add_behaviour"),

    path("update-behaviour", forms.update_behaviour, name="update_behaviour"),

    path("get-behaviours", forms.get_behaviours, name="get_behaviours"),

    path("design-positive-habit", forms.design_positive_habit, name="design_positive_habit"),

    path("design-negative-habit", forms.design_negative_habits, name="design_negative_habits"),

    path("record-todays-habit", forms.record_todays_habit, name="record_todays_habit"),

    path("scale-habit", forms.scale_habit, name="scale_habit"),

    # limiting beliefs
    path("update-beliefs", forms.update_beliefs, name="update_beliefs"),

    # members area chart
    path("three-month-data", forms.get_trimonthly_chart_data, name="get_trimonthly_chart_data"),

    path("weekly-data", forms.get_weekly_chart_data, name="get_weekly_chart_data"),
]

