import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.models import Users, Profile
from .models import *


# Create your views here.
def behaviour_mapping(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        aspiration_name = profile.aspiration_name
        return render(request, 'behaviours/behaviour_mapping.html', {'aspiration_name': aspiration_name})

    return redirect('accounts:sign_in_to_members_area')


def habit_design(request, behaviour_id):
    if request.user.is_authenticated:

        if BehaviourMapping.objects.filter(id=behaviour_id).count() == 0:
            messages.error(request, 'This behavior doesn\'t exists')
            return redirect('main:members_area')

        """get aspiration image"""
        aspiration_image = ''

        behaviour = BehaviourMapping.objects.filter(id=behaviour_id).first()
        if behaviour.value == '+ve':
            print(DesignPositiveHabits.objects.filter(behaviour=behaviour).first())
            content = {'aspirations_image': aspiration_image,
                       'behaviour': BehaviourMapping.objects.filter(id=behaviour_id).first(),
                       'habit_design': DesignPositiveHabits.objects.filter(behaviour=behaviour).first()}
            return render(request, 'behaviours/positive_habit_design.html', content)
        else:
            content = {'aspirations_image': aspiration_image,
                       'behaviour': BehaviourMapping.objects.filter(id=behaviour_id).first(),
                       'habit_design': DesignNegativeHabits.objects.filter(behaviour=behaviour).first()}
            return render(request, 'behaviours/negative_habit_design.html', content)

    return redirect('accounts:sign_in_to_members_area')


def habit_reporting(request, orientation):
    if request.user.is_authenticated:

        """get aspiration image"""
        aspiration_image = ''

        """ensure there is a behaviour"""
        if BehaviourMapping.objects.filter(user=request.user).count() == 0:
            messages.error(request, 'You need to create a behaviour before accessing this page')
            return redirect('main:members_area')

        """ensure all habits are designed"""
        for i in BehaviourMapping.objects.filter(user=request.user).all():
            if i.value == '+ve':
                try:
                    test_habit = i.designpositivehabits
                except Exception as e:
                    messages.error(request,
                                   'You have one or more habits still to design for, please scroll to the habit '
                                   'designer, click the dropdown menus for both positive or negative habits and '
                                   'complete a habit design for each of the listed habits, after this you will be'
                                   ' able review them. Thank you.')
                    return redirect("main:members_area")
            elif i.value == '-ve':
                try:

                    test_habit = i.designnegativehabits
                except Exception as e:
                    messages.error(request,
                                   'You have one or more habits still to design for, please scroll to the habit '
                                   'designer, click the dropdown menus for both positive or negative habits and '
                                   'complete a habit design for each of the listed habits, after this you will be'
                                   ' able review them. Thank you.')
                    return redirect("main:members_area")

        now = datetime.datetime.now()
        today = now.strftime("%A")

        if orientation == 'positive':
            if today.lower() == 'sunday':
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='+ve').all() if
                              i.designpositivehabits.frequency == 'weekly']
            else:
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='+ve').all() if
                              i.designpositivehabits.frequency != 'weekly']

            return render(request, 'behaviours/positive_habit_reporting.html', {'behaviours': behaviours,
                                                                                'aspiration_image': aspiration_image, })

        elif orientation == 'negative':
            if today.lower() == 'sunday':
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='-ve').all() if
                              i.designnegativehabits.frequency == 'weekly']
            else:
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='-ve').all() if
                              i.designnegativehabits.frequency != 'weekly']

            return render(request, 'behaviours/negative_habit_reporting.html', {'behaviours': behaviours,
                                                                                'aspiration_image': aspiration_image, })

        else:
            return render(request, 'main/404.html')

    return redirect('accounts:sign_in_to_members_area')


def habit_summary(request, orientation):
    if request.user.is_authenticated:

        """get aspiration image"""
        aspiration_image = ''

        """ensure there is a behaviour"""
        if BehaviourMapping.objects.filter(user=request.user).count() == 0:
            messages.error(request, 'You need to create a behaviour before accessing this page')
            return redirect('main:members_area')

        """ensure all habits are designed"""
        for i in BehaviourMapping.objects.filter(user=request.user).all():
            if i.value == '+ve':
                try:
                    test_habit = i.designpositivehabits
                except Exception as e:
                    messages.error(request,
                                   'You have one or more habits still to design for, please scroll to the habit '
                                   'designer, click the dropdown menus for both positive or negative habits and '
                                   'complete a habit design for each of the listed habits, after this you will be'
                                   ' able review them. Thank you.')
                    return redirect("main:members_area")
            elif i.value == '-ve':
                try:
                    test_habit = i.designnegativehabits
                except Exception as e:
                    messages.error(request,
                                   'You have one or more habits still to design for, please scroll to the habit '
                                   'designer, click the dropdown menus for both positive or negative habits and '
                                   'complete a habit design for each of the listed habits, after this you will be'
                                   ' able review them. Thank you.')
                    return redirect("main:members_area")

        now = datetime.datetime.now()
        today = now.strftime("%A")
        aspiration_name = request.user.profile.aspiration_name

        if orientation == 'positive':
            if today.lower() == 'sunday':
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='+ve').all() if
                              i.designpositivehabits.frequency == 'weekly']
            else:
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='+ve').all() if
                              i.designpositivehabits.frequency != 'weekly']

            # for habits done today i.e first chart
            selected_behaviors = len(behaviours)
            positive_habits_done_today = str(len([i for i in behaviours if i.done_today])) + '/' + str(
                selected_behaviors)
            first_chart_value = (len([i for i in behaviours if i.done_today]) / selected_behaviors) * 100

            # for habits done this week i.e second chart
            positive_behaviors_done_this_week = request.user.profile.positive_behaviors_done_this_week
            if positive_behaviors_done_this_week == '0/0':
                second_chart_value = 0
            else:
                count = positive_behaviors_done_this_week.split('/')[0]
                count_2 = positive_behaviors_done_this_week.split('/')[1]
                second_chart_value = (int(count) / int(count_2)) * 100

            print(first_chart_value)

            content = {'behaviours': behaviours,
                       'aspiration_image': aspiration_image,
                       'aspiration_name': aspiration_name,
                       'positive_habits_done_today': positive_habits_done_today,
                       'first_chart_value': first_chart_value,
                       'positive_behaviors_done_this_week': positive_behaviors_done_this_week,
                       'second_chart_value': second_chart_value}

            return render(request, 'behaviours/positive_habit_summary.html', content)

        elif orientation == 'negative':
            if today.lower() == 'sunday':
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='-ve').all() if
                              i.designnegativehabits.frequency == 'weekly']
            else:
                behaviours = [i for i in BehaviourMapping.objects.filter(user=request.user, is_selected=True,
                                                                         value='-ve').all() if
                              i.designnegativehabits.frequency != 'weekly']

                # for habits done today i.e first chart
                selected_behaviors = len(behaviours)
                negative_habits_done_today = str(len([i for i in behaviours if i.done_today])) + '/' + str(
                    selected_behaviors)
                first_chart_value = (len([i for i in behaviours if i.done_today]) / selected_behaviors) * 100

                # for habits done this week i.e second chart
                negative_behaviors_done_this_week = request.user.profile.negative_behaviors_done_this_week
                if negative_behaviors_done_this_week == '0/0':
                    second_chart_value = 0
                else:
                    count = negative_behaviors_done_this_week.split('/')[0]
                    count_2 = negative_behaviors_done_this_week.split('/')[1]
                    second_chart_value = (int(count) / int(count_2)) * 100

                print(first_chart_value)

                content = {'behaviours': behaviours,
                           'aspiration_image': aspiration_image,
                           'aspiration_name': aspiration_name,
                           'negative_habits_done_today': negative_habits_done_today,
                           'first_chart_value': first_chart_value,
                           'negative_behaviors_done_this_week': negative_behaviors_done_this_week,
                           'second_chart_value': second_chart_value}

                return render(request, 'behaviours/negative_habit_summary.html', content)
        else:
            return render(request, 'main/404.html')
    return redirect('accounts:sign_in_to_members_area')
