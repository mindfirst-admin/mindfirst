import json

from accounts.models import Users
from apscheduler.schedulers.background import BackgroundScheduler

from characters.models import BehaviourMaps, GoodHabitDesign, BadHabitDesign

bg_work = BackgroundScheduler()
users = Users.objects.all()


def update_daily_behavior_record():
    for user in users:
        good_count = 0
        good_count_all = 0
        bad_count = 0
        bad_count_all = 0

        user_behaviors = BehaviourMaps.objects.filter(user=user, is_selected=True).all()
        for behavior in user_behaviors:
            # for good behaviors
            if behavior.behavior_value == '+ve':
                good_habit = GoodHabitDesign.objects.filter(behavior=behavior).first()
                if good_habit is not None:
                    if good_habit.frequency != 'weekly':
                        good_count_all += 1  # for all  behaviors
                        if behavior.done_today:
                            good_count += 1
            # for bad behaviors
            if behavior.behavior_value == '-ve':
                bad_habit = BadHabitDesign.objects.filter(behavior=behavior).first()
                if bad_habit is not None:
                    if bad_habit.frequency != 'weekly':
                        bad_count_all += 1  # for all  behaviors
                        if behavior.done_today:
                            bad_count += 1

            behavior.done_today = False
            behavior.save()

        good_behaviors_done_this_week = user.profile.good_behaviors_done_this_week
        bad_behaviors_done_this_week = user.profile.bad_behaviors_done_this_week

        try:
            number_of_times_done_prev_day_good = good_behaviors_done_this_week.split('/')[0]
            real_number_of_times_done_prev_day_good = good_behaviors_done_this_week.split('/')[1]

            number_of_times_done_prev_day_bad = bad_behaviors_done_this_week.split('/')[0]
            real_number_of_times_done_prev_day_bad = bad_behaviors_done_this_week.split('/')[1]

            user.profile.good_behaviors_done_this_week = f'{good_count + int(number_of_times_done_prev_day_good)}/{good_count_all + int(real_number_of_times_done_prev_day_good)}'
            user.profile.bad_behaviors_done_this_week = f'{bad_count + int(number_of_times_done_prev_day_bad)}/{bad_count_all + int(real_number_of_times_done_prev_day_bad)}'
            user.profile.save()
        except Exception as e:
            print(e)
            user.profile.good_behaviors_done_this_week = f'{good_count}/{good_count_all}'
            user.profile.bad_behaviors_done_this_week = f'{bad_count}/{bad_count_all}'
            user.profile.save()


def analyze_daily_habit_n_reset_thumb_click():
    for user in users:
        user.profile.red_habits = 0
        user.profile.yellow_habits = 0
        user.profile.green_habits = 0

        user_behaviors = BehaviourMaps.objects.filter(user=user, is_selected=True).all()
        if user_behaviors is not None:
            for behavior in user_behaviors:
                thumbs_up = int(behavior.thumb_up_clicked)
                thumbs_down = int(behavior.thumb_down_clicked)
                if thumbs_up != 0 and thumbs_down != 0:
                    percentage_number = thumbs_up / (thumbs_up + thumbs_down)
                    percentage = percentage_number * 100

                    if 49 >= percentage >= 0:
                        user.profile.red_habits += 1
                    elif 79 >= percentage >= 50:
                        user.profile.yellow_habits += 1
                    elif 100 >= percentage >= 80:
                        user.profile.green_habits += 1
                else:
                    if thumbs_up != 0:
                        user.profile.green_habits += 1
                    elif thumbs_down != 0:
                        user.profile.red_habits += 1
                behavior.thumb_up_clicked = 0
                behavior.thumb_down_clicked = 0
                behavior.save()
        user.profile.save()


def update_daily_chart_using_thumb_clicks():
    for user in users:
        try:
            positive_habits_done = json.loads(user.profile.positive_habits_this_week)
            negative_habits_done = json.loads(user.profile.negative_habits_this_week)
            scaled_habits = json.loads(user.profile.scaled_habits_this_week)

            good_thumbs_up_count = 0
            bad_thumbs_up_count = 0
            scaled_thumbs_up_count = 0

            good_user_behaviors = BehaviourMaps.objects.filter(user=user, is_selected=True, behavior_value='+ve').all()
            if good_user_behaviors is not None:
                for behavior in good_user_behaviors:
                    good_thumbs_up_count += behavior.thumb_up_clicked
                    behavior.thumb_up_clicked = 0
                    behavior.save()

            if any(i.is_scaled == True for i in good_user_behaviors):
                scaled_thumbs_up_count = good_thumbs_up_count
                good_thumbs_up_count = 0

            positive_habits_done.append(good_thumbs_up_count)
            scaled_habits.append(scaled_thumbs_up_count)

            bad_user_behaviors = BehaviourMaps.objects.filter(user=user, is_selected=True, behavior_value='-ve').all()
            if bad_user_behaviors is not None:
                for behavior in bad_user_behaviors:
                    bad_thumbs_up_count += behavior.thumb_down_clicked
                    behavior.thumb_down_clicked = 0
                    behavior.save()

            negative_habits_done.append(bad_thumbs_up_count)

            user.profile.positive_habits_this_week = json.dumps(positive_habits_done)
            user.profile.negative_habits_this_week = json.dumps(negative_habits_done)
            user.profile.scaled_habits_this_week = json.dumps(scaled_habits)

            user.profile.save()
        except Exception as e:
            print(e)


@bg_work.scheduled_job('cron', day_of_week='mon-sat', hour=1, minute=30)
def main():
    update_daily_chart_using_thumb_clicks()
    analyze_daily_habit_n_reset_thumb_click()
    update_daily_behavior_record()


def refresh_behavior_records_weekly():
    for user in users:
        if user.behaviourmaps_set:
            for behavior in user.behaviourmaps_set.all():
                behavior.done_today = False
                behavior.save()
        user.profile.good_behaviors_done_this_week = '0/0'
        user.profile.bad_behaviors_done_this_week = '0/0'

        user.profile.positive_habits_this_week = '[]'
        user.profile.scaled_habits_this_week = '[]'
        user.profile.negative_habits_this_week = '[]'
        user.profile.save()


def update_weekly_chart_using_thumb_clicks():
    for user in users:
        try:
            positive_habits_done = json.loads(user.profile.positive_habits_in_twelve_weeks)
            negative_habits_done = json.loads(user.profile.negative_habits_in_twelve_weeks)
            scaled_habits = json.loads(user.profile.scaled_habits_in_twelve_weeks)

            good_thumbs_up_count = 0
            bad_thumbs_up_count = 0
            scaled_thumbs_up_count = 0

            good_user_behaviors = BehaviourMaps.objects.filter(user=user, is_selected=True, behavior_value='+ve').all()
            if good_user_behaviors is not None:
                for behavior in good_user_behaviors:
                    good_thumbs_up_count += behavior.thumb_up_week
                    behavior.thumb_up_week = 0
                    behavior.save()

            if any(i.is_scaled == True for i in good_user_behaviors):
                scaled_thumbs_up_count = good_thumbs_up_count
                good_thumbs_up_count = 0

            positive_habits_done.append(good_thumbs_up_count)
            scaled_habits.append(scaled_thumbs_up_count)

            bad_user_behaviors = BehaviourMaps.objects.filter(user=user, is_selected=True, behavior_value='-ve').all()
            if bad_user_behaviors is not None:
                for behavior in bad_user_behaviors:
                    bad_thumbs_up_count += behavior.thumb_down_week
                    behavior.thumb_down_week = 0
                    behavior.save()

            negative_habits_done.append(bad_thumbs_up_count)

            user.profile.positive_habits_in_twelve_weeks = json.dumps(positive_habits_done)
            user.profile.negative_habits_in_twelve_weeks = json.dumps(negative_habits_done)
            user.profile.scaled_habits_in_twelve_weeks = json.dumps(scaled_habits)

            user.profile.save()
        except Exception as e:
            print(e)


@bg_work.scheduled_job('cron', day_of_week='sun', hour=23, minute=55)
def weekly():
    update_weekly_chart_using_thumb_clicks()
    refresh_behavior_records_weekly()
