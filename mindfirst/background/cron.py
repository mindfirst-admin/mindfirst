import json

from accounts.models import Users
from apscheduler.schedulers.background import BackgroundScheduler

from behaviours.models import *

scheduled = BackgroundScheduler()
users = Users.objects.all()


# daily
def update_daily_behavior_record():
    for user in users:
        positive_habits_done_count = 0  # for positive habits done the prev day
        all_selected_positive_habits = 0  # for all selected positive behaviours
        negative_habits_n_done_count = 0  # for negative habits not done the prev day
        all_selected_negative_habits = 0  # for all selected negative behaviours

        user_behaviours = BehaviourMapping.objects.filter(user=user, is_selected=True).all()
        for behaviour in user_behaviours:
            # for positive behaviors
            if behaviour.value == '+ve':
                good_behaviour = DesignPositiveHabits.objects.filter(behaviour=behaviour).first()
                if good_behaviour is not None:
                    if good_behaviour.frequency != 'weekly':
                        all_selected_positive_habits += 1
                        if behaviour.done_today:
                            positive_habits_done_count += 1

            # for negative behaviors
            elif behaviour.value == '-ve':
                bad_behaviour = DesignNegativeHabits.objects.filter(behaviour=behaviour).first()
                if bad_behaviour is not None:
                    if bad_behaviour.frequency != 'weekly':
                        all_selected_negative_habits += 1
                        if behaviour.done_today:
                            negative_habits_n_done_count += 1

            # resetting it for new day
            behaviour.done_today = False
            behaviour.save()

        # adding to weeks total
        positive_behaviours_done_this_week = user.profile.positive_behaviors_done_this_week
        negative_behaviours_done_this_week = user.profile.negative_behaviors_done_this_week

        try:
            # if there was data already present
            # getting previous positive habit data
            positive_habits_weekly_total = int(positive_behaviours_done_this_week.split('/')[0])
            positive_selected_habits_weekly_total = int(positive_behaviours_done_this_week.split('/')[1])

            # getting previous negative habit data
            negative_habits_weekly_total = int(negative_behaviours_done_this_week.split('/')[0])
            negative_selected_habits_weekly_total = int(negative_behaviours_done_this_week.split('/')[1])

            # incrementing positive habits profile
            positive_habits_weekly_total = positive_habits_weekly_total + positive_habits_done_count
            positive_selected_habits_weekly_total = positive_selected_habits_weekly_total + all_selected_positive_habits
            user.profile.positive_behaviors_done_this_week = f'{positive_habits_weekly_total}/' \
                                                             f'{positive_selected_habits_weekly_total}'

            # incrementing negative habits profile
            negative_habits_weekly_total = negative_habits_weekly_total + negative_habits_n_done_count
            negative_selected_habits_weekly_total = negative_selected_habits_weekly_total + all_selected_negative_habits
            user.profile.negative_behaviors_done_this_week = f'{negative_habits_weekly_total}/' \
                                                             f'{negative_selected_habits_weekly_total}'

            # save
            user.profile.save()
        except Exception as e:  # some django exception
            # new weeks data
            user.profile.positive_behaviors_done_this_week = f'{positive_habits_done_count}/' \
                                                             f'{all_selected_positive_habits}'
            user.profile.negative_behaviors_done_this_week = f'{negative_habits_n_done_count}/' \
                                                             f'{all_selected_negative_habits}'
            user.profile.save()


def update_daily_chart_using_thumb_clicks():
    for user in users:
        try:
            # retrieving previous data from profile
            positive_habits_done = json.loads(user.profile.all_positive_habits_this_week)
            negative_habits_done = json.loads(user.profile.all_negative_habits_this_week)
            scaled_habits = json.loads(user.profile.all_scaled_habits_this_week)

            positive_thumbs_up_count = 0
            negative_thumbs_up_count = 0
            scaled_thumbs_up_count = 0

            # getting positive behaviours with thumbs up on prev day
            positive_user_behaviours = BehaviourMapping.objects.filter(user=user, is_selected=True, value='+ve').all()
            if positive_user_behaviours is not None:
                for behaviour in positive_user_behaviours:
                    positive_thumbs_up_count += behaviour.thumbs_up_today

            # checking if behaviour is scaled so its moved to scaled list
            if any(i.is_scaled == True for i in positive_user_behaviours):
                # this is done for easier representation on chart
                scaled_thumbs_up_count = positive_thumbs_up_count
                positive_thumbs_up_count = 0

            # appending data to previous data on list
            positive_habits_done.append(positive_thumbs_up_count)
            scaled_habits.append(scaled_thumbs_up_count)

            # getting negative behaviours with thumbs up on prev day
            negative_user_behaviours = BehaviourMapping.objects.filter(user=user, is_selected=True, value='-ve').all()
            if negative_user_behaviours is not None:
                for behaviour in negative_user_behaviours:
                    negative_thumbs_up_count += behaviour.thumbs_down_today

            # appending data to previous data on list
            negative_habits_done.append(negative_thumbs_up_count)

            # entering new data to profile
            user.profile.all_positive_habits_this_week = json.dumps(positive_habits_done)
            user.profile.all_negative_habits_this_week = json.dumps(negative_habits_done)
            user.profile.all_scaled_habits_this_week = json.dumps(scaled_habits)

            user.profile.save()
        except Exception as e:
            pass


def analyze_daily_habit_n_reset_thumb_click():
    for user in users:
        user.profile.red_habits = 0
        user.profile.yellow_habits = 0
        user.profile.green_habits = 0
        user.profile.scaled_habits = 0

        user_behaviour = BehaviourMapping.objects.filter(user=user, is_selected=True).all()
        if user_behaviour is not None:
            for behaviour in user_behaviour:
                thumbs_up = int(behaviour.thumbs_up_today)
                thumbs_down = int(behaviour.thumbs_down_today)

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

                if behaviour.is_scaled:
                    user.profile.scaled_habits += 1

                behaviour.thumbs_up_today = 0
                behaviour.thumbs_down_today = 0
                behaviour.save()
        user.profile.save()


@scheduled.scheduled_job('cron', day_of_week='mon-sat', hour=23, minute=59)
def daily():
    update_daily_behavior_record()
    update_daily_chart_using_thumb_clicks()
    analyze_daily_habit_n_reset_thumb_click()


# weekly
def weekly_record_refresh():
    for user in users:
        user_behaviours = BehaviourMapping.objects.filter(user=user).all()
        if user_behaviours is not None:
            for behaviour in user_behaviours:
                behaviour.done_today = False
                behaviour.save()

        user.profile.positive_behaviors_done_this_week = '0/0'
        user.profile.negative_behaviors_done_this_week = '0/0'

        user.profile.all_positive_habits_this_week = '[]'
        user.profile.all_scaled_habits_this_week = '[]'
        user.profile.all_negative_habits_this_week = '[]'
        user.profile.save()


def update_twelve_week_chart_using_thumb_clicks():
    for user in users:
        try:
            positive_habits_done = json.loads(user.profile.all_positive_habits_in_twelve_weeks)
            negative_habits_done = json.loads(user.profile.all_negative_habits_in_twelve_weeks)
            scaled_habits = json.loads(user.profile.all_scaled_habits_in_twelve_weeks)

            positive_thumbs_up_count = 0
            negative_thumbs_up_count = 0
            scaled_thumbs_up_count = 0

            # getting positive behaviours with thumbs up on prev day
            positive_user_behaviours = BehaviourMapping.objects.filter(user=user, is_selected=True, value='+ve').all()
            if positive_user_behaviours is not None:
                for behaviour in positive_user_behaviours:
                    positive_thumbs_up_count += behaviour.thumbs_up_this_week

            # checking if behaviour is scaled so its moved to scaled list
            if any(i.is_scaled == True for i in positive_user_behaviours):
                # this is done for easier representation on chart
                scaled_thumbs_up_count = positive_thumbs_up_count
                positive_thumbs_up_count = 0

            # appending data to previous data on list
            positive_habits_done.append(positive_thumbs_up_count)
            scaled_habits.append(scaled_thumbs_up_count)

            # getting negative behaviours with thumbs up on prev day
            negative_user_behaviours = BehaviourMapping.objects.filter(user=user, is_selected=True, value='-ve').all()
            if negative_user_behaviours is not None:
                for behaviour in negative_user_behaviours:
                    negative_thumbs_up_count += behaviour.thumbs_down_this_week

            # appending data to previous data on list
            negative_habits_done.append(negative_thumbs_up_count)

            # entering new data to profile
            user.profile.all_positive_habits_in_twelve_weeks = json.dumps(positive_habits_done)
            user.profile.all_negative_habits_in_twelve_weeks = json.dumps(negative_habits_done)
            user.profile.all_scaled_habits_in_twelve_weeks = json.dumps(scaled_habits)

            user.profile.save()
        except Exception as e:
            pass


@scheduled.scheduled_job('cron', day_of_week='sun', hour=23, minute=55)
def weekly():
    weekly_record_refresh()
    update_twelve_week_chart_using_thumb_clicks()


# trimonthly
"""Todo: make scheduler for 3 months"""
