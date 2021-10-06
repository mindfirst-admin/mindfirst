"""
# for values images
from django.shortcuts import render, redirect
from accounts.models import Profile
from django.conf import settings
from django.contrib.auth import logout
from accounts.extras_ import *
from user_files.models import UserFiles
import glob
from pathlib import Path


# Create your views here.
def home(response):
    if response.user.is_authenticated:
        return render(response, 'main/home.html', {})
    else:
        return redirect('main:login')


def members_area(response):
    if response.user.is_authenticated:
        aspiration_files = UserFiles.objects.filter(user=response.user, file_category='aspirations').all()
        video_file = UserFiles.objects.filter(user=response.user, file_category='gallery_video').first()
        profile = Profile.objects.get(user=response.user)

        if len(aspiration_files) == 0:
            aspiration_image = 'main/assets/landing_image.jpg'
        else:
            aspiration_image = aspiration_files[0]

        if not video_file:
            has_video = False
        else:
            has_video = True

        scaled_habits = profile.scaled_habits
        green_habits = profile.green_habits
        yellow_habits = profile.yellow_habits
        red_habits = profile.red_habits

        context = {'vision_gallery_video': video_file,
                   'has_video': has_video,
                   'scaled_habits': scaled_habits,
                   'green_habits': green_habits,
                   'yellow_habits': yellow_habits,
                   'red_habits': red_habits,
                   'aspiration_image': aspiration_image
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
        user_value_files = [i.file for i in
                            UserFiles.objects.filter(user=response.user, file_category='values').all()]
        user_value_files_stripped =  [i.split('/')[-1] for i in user_value_files]
        admin_value_files = [i.replace('main/media/', '') for i in
                             glob.glob('main/media/admin/values/*.*', recursive=True)]

        value_files = []

        for file in admin_value_files:
            file_name = file.split('/')[-1]
            for file_name_ in user_value_files:
                file_name__ = file_name_.split('/')[-1]
                            if file_name in user_value_files_stripped:
                class ImageMeta:
                    url = user_value_files[user_value_files_stripped.index(file_name)]
                    check = True
                    name = file_name
            else:
                class ImageMeta:
                    url = file
                    check = False
                    name = file_name
            image_files.append(ImageMeta)
                value_files.append(image_meta)

        return render(response, 'main/edit_values.html', {'images': value_files})
    else:
        return redirect('main:login')


def watch_video(response):
    if response.user.is_authenticated:
        vision_gallery_video_path = f'main/static/all_user_files/{str(response.user.id)}/start_video'
        vision_gallery_video = [i.replace('main/static/', '')
                                for i in glob.glob(vision_gallery_video_path + '/*.*', recursive=True)][0]

        return render(response, 'main/watch_video.html', {'vision_gallery_video': vision_gallery_video})
    else:
        return redirect('main:login')


def processing_video(response):
    if response.user.is_authenticated:
        return render(response, 'main/processing_video.html', {})
    else:
        return redirect('main:login')


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


def verify_user(response, user_token):
    try:
        user_profile = Profile.objects.filter(user_token=user_token).first()
        email = user_profile.user.email
        token = user_token
        return render(response, 'main/verification.html', {'email': email, 'token': token})
    except AttributeError:
        return render(response, 'main/404.html', )


def forgot_password_show(response):
    return render(response, 'main/forgot-password.html', {})


def forgot_password(response, user_token):
    try:
        user_profile = Profile.objects.filter(user_token=user_token).first()
        email = user_profile.user.email
        token = user_token
        return render(response, 'main/reset-password.html', {'email': email, 'token': token})
    except AttributeError:
        return render(response, 'main/404.html', )


def terms_and_conditions(response):
    return render(response, 'main/terms.html', {})


def logout_user(request):
    logout(request)
    return redirect('main:login')

"""