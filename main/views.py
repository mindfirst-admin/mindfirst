import os

from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.models import Profile
from django.conf import settings
from django.contrib.auth import logout
from accounts.extras_ import *
from user_files.models import UserFiles
from characters.models import BehaviourMaps, LimitingBeliefs, GoodHabitDesign, BadHabitDesign
from page_structures.models import *
import glob
import datetime
from pathlib import Path


# Create your views here.
def home(response):
    return render(response, 'main/home.html', {})


def members_area(response):
    if response.user.is_authenticated:
        aspiration_files = UserFiles.objects.filter(user=response.user, file_category='aspirations').all()
        video_file = UserFiles.objects.filter(user=response.user, file_category='video').first()
        profile = Profile.objects.get(user=response.user)

        if len(aspiration_files) == 0:
            aspiration_image = 'main/assets/landing_image.jpg'
        else:
            aspiration_image = 'media/' + str(aspiration_files[0].file)

        if not video_file:
            has_video = False
        else:
            has_video = True

        scaled_habits = BehaviourMaps.objects.filter(user=response.user, is_selected=True, is_scaled=True).count()
        green_habits = profile.green_habits
        yellow_habits = profile.yellow_habits
        red_habits = profile.red_habits

        aspiration_name = profile.aspiration_name
        behaviors_list = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True).all()]

        context = {
            'vision_gallery_video': video_file,
            'has_video': has_video,
            'scaled_habits': scaled_habits,
            'green_habits': green_habits,
            'yellow_habits': yellow_habits,
            'red_habits': red_habits,
            'aspiration_image': aspiration_image,
            'aspiration_name': aspiration_name,
            'behaviors_list': behaviors_list,
        }
        return render(response, 'main/members.html', context)
    else:
        return redirect('main:login')


def vision_gallery(response):
    if response.user.is_authenticated:
        aspiration_files = UserFiles.objects.filter(user=response.user, file_category='aspirations').all()
        values_files = UserFiles.objects.filter(user=response.user, file_category='values').all()

        context = {
            'aspirations': aspiration_files,
            'values': values_files
        }

        return render(response, 'main/vision_gallery.html', context)
    else:
        return redirect('main:login')


def edit_aspirations(response):
    if response.user.is_authenticated:
        aspiration_files = UserFiles.objects.filter(user=response.user, file_category='aspirations').all()

        return render(response, 'main/edit_aspirations.html', {'aspirations': aspiration_files})
    else:
        return redirect('main:login')


def edit_values(response):
    if response.user.is_authenticated:
        user_value_files = [str(i.file) for i in
                            UserFiles.objects.filter(user=response.user, file_category='values').all()]
        admin_value_files = [i.replace(settings.MEDIA_REL_PATH, '') for i in
                             glob.glob(settings.MEDIA_REL_PATH + 'admin/values/*.*', recursive=True)]

        user_value_files_stripped = [os.path.basename(i) for i in user_value_files]

        image_files = []

        for file in admin_value_files:
            file_name = os.path.basename(Path(file))
            if file_name in user_value_files_stripped:
                image_meta = {
                    'url': file,
                    'check': True,
                    'name': file_name
                }
            else:
                image_meta = {
                    'url': file,
                    'check': False,
                    'name': file_name
                }
            image_files.append(image_meta)

        return render(response, 'main/edit_values.html', {'images': image_files})
    else:
        return redirect('main:login')


def watch_video(response):
    if response.user.is_authenticated:
        video_file = UserFiles.objects.filter(user=response.user, file_category='video').first()

        return render(response, 'main/watch_video.html', {'video_file': video_file})
    else:
        return redirect('main:login')


def processing_video(response):
    if response.user.is_authenticated:
        return render(response, 'main/processing_video.html', {})
    else:
        return redirect('main:login')


def behaviour_mapping(response):
    if response.user.is_authenticated:
        profile = Profile.objects.get(user=response.user)
        aspiration_name = profile.aspiration_name
        return render(response, 'main/behaviour_mapping.html', {'aspiration_name': aspiration_name})
    else:
        return redirect('main:login')


def habit_design(response):
    if response.user.is_authenticated:
        try:
            b_id = response.session['behavior_id']
            behavior = BehaviourMaps.objects.filter(user=response.user, id=b_id).first()

            aspiration_image = UserFiles.objects.filter(user=response.user, file_category='aspirations').first()

            if not aspiration_image:
                messages.error(response, 'You need to set an aspiration image')
                return redirect("main:members_area")

            if behavior.behavior_value == '+ve':
                habit_design = GoodHabitDesign.objects.filter(behavior=behavior).first()
                return render(response, 'main/good_habit_designer.html', {
                    'behavior': behavior,
                    'aspiration_image': aspiration_image.file,
                    'habit_design': habit_design,
                })
            else:
                habit_design = BadHabitDesign.objects.filter(behavior=behavior).first()
                return render(response, 'main/bad_habit_designer.html', {
                    'behavior': behavior,
                    'aspiration_image': aspiration_image.file,
                    'habit_design': habit_design,
                })
        except KeyError as e:
            return redirect("main:members_area")
    else:
        return redirect('main:login')


def habit_reporting(response):
    if response.user.is_authenticated:
        now = datetime.datetime.now()
        today = now.strftime("%A")

        try:
            if today != 'Sunday':
                behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                     behavior_value='+ve').all() if
                             i.goodhabitdesign.frequency != 'weekly']
            else:
                behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                     behavior_value="+ve").all()]
        except Exception as e:
            print(e)
            messages.error(response,
                           'You have one or more habits still to design for, please scroll to the habit designer, click the dropdown menus for both positive or negative habits and complete a habit design for each of the listed habits, after this you will be able review them. Thank you.')
            return redirect("main:members_area")

        aspiration_image = UserFiles.objects.filter(user=response.user, file_category='aspirations').first()

        if not aspiration_image:
            messages.error(response, 'You need to set an aspiration image')
            return redirect("main:members_area")

        for i in behaviors:
            try:
                p = i.goodhabitdesign
            except Exception as e:
                print(e)
                messages.error(response,
                               'You have one or more habits still to design for, please scroll to the habit designer, click the dropdown menus for both positive or negative habits and complete a habit design for each of the listed habits, after this you will be able review them. Thank you.')
                return redirect("main:members_area")

        return render(response, 'main/habit_reporting.html', {
            'behaviors': behaviors,
            'aspiration_image': aspiration_image.file,
        })
    else:
        return redirect('main:login')


def bad_habit_reporting(response):
    if response.user.is_authenticated:
        now = datetime.datetime.now()
        today = now.strftime("%A")

        try:
            if today != 'Sunday':
                behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                     behavior_value='-ve').all() if
                             i.badhabitdesign.frequency != 'weekly']
            else:
                behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                     behavior_value="-ve").all()]
        except Exception as e:
            print(e)
            messages.error(response,
                           'You have one or more habits still to design for, please scroll to the habit designer, click the dropdown menus for both positive or negative habits and complete a habit design for each of the listed habits, after this you will be able review them. Thank you.')
            return redirect("main:members_area")

        aspiration_image = UserFiles.objects.filter(user=response.user, file_category='aspirations').first()

        if not aspiration_image:
            messages.error(response, 'You need to set an aspiration image')
            return redirect("main:members_area")

        for i in behaviors:
            try:
                p = i.badhabitdesign.frequency
            except Exception as e:
                messages.error(response,
                               'You have one or more habits still to design for, please scroll to the habit designer, click the dropdown menus for both positive or negative habits and complete a habit design for each of the listed habits, after this you will be able review them. Thank you.')
                return redirect("main:members_area")

        return render(response, 'main/bad_habit_reporting.html', {
            'behaviors': behaviors,
            'aspiration_image': aspiration_image.file,
        })
    else:
        return redirect('main:login')


def habit_summary(response):
    if response.user.is_authenticated:

        now = datetime.datetime.now()
        today = now.strftime("%A")
        if today != 'Sunday':
            good_behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                      behavior_value="+ve").all() if
                              i.goodhabitdesign.frequency != 'weekly']
        else:
            good_behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                      behavior_value="+ve").all()]

        aspiration_image = UserFiles.objects.filter(user=response.user, file_category='aspirations').first()
        aspiration_name = response.user.profile.aspiration_name

        good_behaviors_done_this_week = response.user.profile.good_behaviors_done_this_week

        # for habits done today
        good_selected_behaviors = len(good_behaviors)

        good_habits_done = [i for i in good_behaviors if i.done_today]

        if len(good_habits_done) >= good_selected_behaviors:
            good_habits_done_length = good_selected_behaviors
        else:
            good_habits_done_length = len(good_habits_done)

        if good_behaviors_done_this_week == '0/0':
            good_weekly_summary = 0
        else:
            count = good_behaviors_done_this_week.split('/')[0]
            count_2 = good_behaviors_done_this_week.split('/')[1]
            good_weekly_summary = (int(count) / int(count_2)) * 100

        good_today_summary = (good_habits_done_length / good_selected_behaviors) * 100

        if not aspiration_image:
            messages.error(response, 'You need to set an aspiration image')
            return redirect("main:members_area")

        class GoodBehaviorForm:
            behaviors = good_behaviors
            selected_behaviors = good_selected_behaviors
            today_summary = good_today_summary
            behaviors_done_this_week = good_behaviors_done_this_week
            weekly_summary = good_weekly_summary
            habits_done_length = good_habits_done_length

        return render(response, 'main/habit_summary.html', {
            'aspiration_image': aspiration_image.file,
            'aspiration_name': aspiration_name,
            'good_behavior_form': GoodBehaviorForm(),
        })
    else:
        return redirect('main:login')


def bad_habit_summary(response):
    if response.user.is_authenticated:

        now = datetime.datetime.now()
        today = now.strftime("%A")
        if today != 'Sunday':
            bad_behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                     behavior_value="-ve").all() if
                             i.badhabitdesign.frequency != 'weekly']
        else:
            bad_behaviors = [i for i in BehaviourMaps.objects.filter(user=response.user, is_selected=True,
                                                                     behavior_value="-ve").all()]

        aspiration_image = UserFiles.objects.filter(user=response.user, file_category='aspirations').first()
        aspiration_name = response.user.profile.aspiration_name

        bad_behaviors_done_this_week = response.user.profile.bad_behaviors_done_this_week

        # for habits done today
        bad_selected_behaviors = len(bad_behaviors)

        bad_habits_done = [i for i in bad_behaviors if i.done_today]

        if len(bad_habits_done) >= bad_selected_behaviors:
            bad_habits_done_length = bad_selected_behaviors
        else:
            bad_habits_done_length = len(bad_habits_done)

        if bad_behaviors_done_this_week == '0/0':
            bad_weekly_summary = 0
        else:
            count = bad_behaviors_done_this_week.split('/')[0]
            count_2 = bad_behaviors_done_this_week.split('/')[1]
            bad_weekly_summary = (int(count) / int(count_2)) * 100

        bad_today_summary = (bad_habits_done_length / bad_selected_behaviors) * 100

        if not aspiration_image:
            messages.error(response, 'You need to set an aspiration image')
            return redirect("main:members_area")

        class BadBehaviorForm:
            behaviors = bad_behaviors
            selected_behaviors = bad_selected_behaviors
            today_summary = bad_today_summary
            behaviors_done_this_week = bad_behaviors_done_this_week
            weekly_summary = bad_weekly_summary
            habits_done_length = bad_habits_done_length

        return render(response, 'main/bad-habit-summary.html', {
            'aspiration_image': aspiration_image.file,
            'aspiration_name': aspiration_name,
            'bad_behavior_form': BadBehaviorForm(),
        })
    else:
        return redirect('main:login')


def limiting_beliefs(response):
    if response.user.is_authenticated:
        belief = LimitingBeliefs.objects.filter(user=response.user).first()
        if belief is not None:
            data = belief.beliefs
        else:
            data = ['12 Love']
            nums = [5, 4, 3, 2, 2]
            words = ('Liebe,ፍቅር,Lufu,حب,Aimor,Amor,Heyran,ভালোবাসা,Каханне,Любоў,Любов,བརྩེ་དུང་།,' +
                     'Ljubav,Karantez,Юрату,Láska,Amore,Cariad,Kærlighed,Armastus,Αγάπη,Amo,Amol,Maitasun,' +
                     'عشق,Pyar,Amour,Leafde,Gràdh,愛,爱,પ્રેમ,사랑,Սեր,Ihunanya,Cinta,ᑕᑯᑦᓱᒍᓱᑉᐳᖅ,Ást,אהבה,' +
                     'ಪ್ರೀತಿ,სიყვარული,Махаббат,Pendo,Сүйүү,Mīlestība,Meilė,Leefde,Bolingo,Szerelem,' +
                     'Љубов,സ്നേഹം,Imħabba,प्रेम,Ái,Хайр,အချစ်,Tlazohtiliztli,Liefde,माया,मतिना,' +
                     'Kjærlighet,Kjærleik,ପ୍ରେମ,Sevgi,ਪਿਆਰ,پیار,Miłość,Leevde,Dragoste,' +
                     'Khuyay,Любовь,Таптал,Dashuria,Amuri,ආදරය,Ljubezen,Jaceyl,خۆشەویستی,Љубав,Rakkaus,' +
                     'Kärlek,Pag-ibig,காதல்,ప్రేమ,ความรัก,Ишқ,Aşk,محبت,Tình yêu,Higugma,ליבע').split(',')
            for num in nums:
                for word in words:
                    data.append(str(num) + ' ' + str(word))
            data = '\n'.join(data)
        return render(response, 'main/limiting_beliefs.html', {'data': data})
    else:
        return redirect('main:login')


def take_control(response, week):
    if response.user.is_authenticated:
        week = WeekModel.objects.filter(week_id=week).first()
        if week is not None:
            folder = FolderModel.objects.filter(week=week).all()
            w_learn = WhatYoullLearnModel.objects.filter(week=week).all()
            main_title = 'Take Control Over Your Habits'

            file_name, extension = os.path.splitext(str(week.file))
            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(response, 'main/week.html',
                          {'day': week, 'folder': folder, 'w_learn': w_learn, 'main_title': main_title,
                           'sub_title': week.title, 'is_video': is_video})
        else:
            return render(response, 'main/404.html', {})
    else:
        return redirect('main:login')


def mind_workshop(response, week):
    if response.user.is_authenticated:
        week = MindWorkshopModel.objects.filter(week_id=week).first()
        if week is not None:
            folder = FolderModel.objects.filter(mind_workshop=week).all()
            w_learn = WhatYoullLearnModel.objects.filter(mind_workshop=week).all()
            main_title = 'Mind Workshop'

            file_name, extension = os.path.splitext(str(week.file))
            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(response, 'main/week.html',
                          {'day': week, 'folder': folder, 'w_learn': w_learn, 'main_title': main_title,
                           'sub_title': week.title, 'is_video': is_video})
        else:
            return render(response, 'main/404.html', {})
    else:
        return redirect('main:login')


def day_(response, day):
    if response.user.is_authenticated:
        day = DayModel.objects.filter(day_id=day).first()
        if day is not None:
            folder = FolderModel.objects.filter(day=day).all()
            w_learn = WhatYoullLearnModel.objects.filter(day=day).all()
            main_title = day.title.split(' - ')[1]
            sub_title = day.title.split(' - ')[0]

            file_name, extension = os.path.splitext(str(day.file))
            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(response, 'main/days.html',
                          {'day': day, 'folder': folder, 'w_learn': w_learn, 'main_title': main_title,
                           'sub_title': sub_title, 'is_video': is_video})
        else:
            return render(response, 'main/404.html', {})
    else:
        return redirect('main:login')


def five_day(response, day):
    if response.user.is_authenticated:
        day = FiveDayModel.objects.filter(day_id=day).first()
        if day is not None:
            folder = FolderModel.objects.filter(five_day=day).all()
            w_learn = WhatYoullLearnModel.objects.filter(five_day=day).all()
            main_title = '5-Day Challenge'
            sub_title = day.title

            file_name, extension = os.path.splitext(str(day.file))
            is_video = False
            if extension == '.mp4':
                is_video = True

            return render(response, 'main/days.html',
                          {'day': day, 'folder': folder, 'w_learn': w_learn, 'main_title': main_title,
                           'sub_title': sub_title, 'is_video': is_video})
        else:
            return render(response, 'main/404.html', {})
    else:
        return redirect('main:login')


def products(response):
    return render(response, 'main/products.html', {})


def book(response):
    return render(response, 'main/book.html', {})


def details(response, product):
    main_header = ''
    sub_header = ''
    text = ''
    link = '#'

    if product == '5-day-challenge':
        main_header = '5-Day Challenge'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        text = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
               'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
               ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
               'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
               'and may cause you to resist new ways of doing things.'
        link = '#'

    elif product == 'book':
        main_header = 'Progress Equals Happiness'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        text = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
               'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
               ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
               'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
               'and may cause you to resist new ways of doing things.'
        link = '#'

    elif product == 'workbook':
        main_header = 'Our Workbook'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        text = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
               'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
               ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
               'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
               'and may cause you to resist new ways of doing things.'
        link = '#'

    elif product == 'membership':
        main_header = 'Mind First Membership'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        text = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
               'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
               ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
               'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
               'and may cause you to resist new ways of doing things.'
        link = '#'

    return render(response, 'main/details.html', {
        'main_header': main_header,
        'sub_header': sub_header,
        'text': text,
        'link': link
    })


def login(response):
    return render(response, 'main/login.html', {})


def sign_up(response):
    return render(response, 'main/register.html', {})


def add_payment(response):
    return render(response, 'main/payment.html', {})


def payment_successful(response):
    details = response.session['new_profile']
    print(details['password'])
    send_password_mail(details['password'], details['email'])
    send_welcome_email(details['email'])
    return render(response, 'main/success.html', {})


def payment_unsuccessful(response):
    return render(response, 'main/failed.html', {})


def forgot_password_show(response):
    return render(response, 'main/forgot-password.html', {})


def terms_and_conditions(response):
    return render(response, 'main/terms.html', {})


def logout_user(request):
    logout(request)
    return redirect('main:login')
