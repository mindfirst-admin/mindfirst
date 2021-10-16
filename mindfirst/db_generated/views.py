import os

from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def take_control_over_your_habits(request, week_id):
    if request.user.is_authenticated:
        week_data = WeekModel.objects.filter(week_id=week_id).first()

        if week_data is not None:
            # getting resources and what you'll learn image/video and text
            resources = ResourcesModel.objects.filter(week=week_data).all()
            w_y_learn = WhatYoullLearnModel.objects.filter(week=week_data).all()

            # for the header on page
            main_title = 'Take Control Over Your Habits'

            # checking if that weeks file is a video or not
            file_name, extension = os.path.splitext(str(week_data.file))

            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(request, 'template_pages/video_template.html',
                          {'data': week_data, 'resources': resources, 'w_y_learn': w_y_learn, 'main_title': main_title,
                           'sub_title': week_data.title, 'is_video': is_video})
        else:
            return render(request, 'main/404.html', {})
    else:
        return redirect('accounts:sign_in_to_members_area')


def mind_workshop(request, week_id):
    if request.user.is_authenticated:
        week_data = MindWorkshopModel.objects.filter(week_id=week_id).first()

        if week_data is not None:
            # getting resources and what you'll learn image/video and text
            resources = ResourcesModel.objects.filter(mind_workshop=week_data).all()
            w_y_learn = WhatYoullLearnModel.objects.filter(mind_workshop=week_data).all()

            # for the header on page
            main_title = 'Mind Workshop'

            # checking if that weeks file is a video or not
            file_name, extension = os.path.splitext(str(week_data.file))

            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(request, 'template_pages/video_template.html',
                          {'data': week_data, 'resources': resources, 'w_y_learn': w_y_learn, 'main_title': main_title,
                           'sub_title': week_data.title, 'is_video': is_video})
        else:
            return render(request, 'main/404.html', {})
    else:
        return redirect('accounts:sign_in_to_members_area')


def day_(request, day_id):
    if request.user.is_authenticated:
        day_data = DayModel.objects.filter(day_id=day_id).first()

        if day_data is not None:
            # getting resources and what you'll learn image/video and text
            resources = ResourcesModel.objects.filter(day=day_data).all()
            w_y_learn = WhatYoullLearnModel.objects.filter(day=day_data).all()

            # header and sub header
            main_title = day_data.title.strip().split('-')[1]
            sub_title = day_data.title.strip().split('-')[0]

            # checking if that days file is a video or not
            file_name, extension = os.path.splitext(str(day_data.file))
            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(request, 'template_pages/template.html',
                          {'data': day_data, 'resources': resources, 'w_y_learn': w_y_learn, 'main_title': main_title,
                           'sub_title': sub_title, 'is_video': is_video})
        else:
            return render(request, 'main/404.html', {})
    else:
        return redirect('accounts:sign_in_to_members_area')


def five_day(request, day_id):
    if request.user.is_authenticated:
        day_data = FiveDayModel.objects.filter(day_id=day_id).first()

        if day_data is not None:
            # getting resources and what you'll learn image/video and text
            resources = ResourcesModel.objects.filter(five_day=day_data).all()
            w_y_learn = WhatYoullLearnModel.objects.filter(five_day=day_data).all()

            # header and sub header
            main_title = 'Five Days Challenge'
            sub_title = day_data.title

            # checking if that days file is a video or not
            file_name, extension = os.path.splitext(str(day_data.file))
            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(request, 'template_pages/template.html',
                          {'data': day_data, 'resources': resources, 'w_y_learn': w_y_learn, 'main_title': main_title,
                           'sub_title': sub_title, 'is_video': is_video})
        else:
            return render(request, 'main/404.html', {})
    else:
        return redirect('accounts:sign_in_to_members_area')
