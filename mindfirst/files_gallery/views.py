import os

from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def vision_gallery(request):
    if request.user.is_authenticated:
        aspiration_images = VisionGalleryFiles.objects.filter(user=request.user, file_category='aspirations').all()
        values_images = VisionGalleryFiles.objects.filter(user=request.user, file_category='values').all()

        content = {
            'aspiration_images': aspiration_images,
            'values_images': values_images
        }

        return render(request, 'user_files/vision_gallery.html', content)
    else:
        return redirect('accounts:sign_in_to_members_area')


def edit_aspirations(request):
    if request.user.is_authenticated:
        aspiration_files = VisionGalleryFiles.objects.filter(user=request.user, file_category='aspirations').all()

        return render(request, 'user_files/edit_aspirations.html', {'aspirations': aspiration_files})
    else:
        return redirect('accounts:sign_in_to_members_area')


def edit_values(response):
    if response.user.is_authenticated:
        user_value_files = [str(i.file) for i in
                            VisionGalleryFiles.objects.filter(user=response.user, file_category='values').all()]
        admin_value_files = [str(i.image) for i in AdminValuesImages.objects.all()]

        user_value_files_stripped = [os.path.basename(i) for i in user_value_files]  # getting the file names

        values_image_files = []

        for file in admin_value_files:
            file_name = os.path.basename(file)
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
            values_image_files.append(image_meta)

        return render(response, 'user_files/edit_values.html', {'images': values_image_files})
    else:
        return redirect('accounts:sign_in_to_members_area')


def watch_video(response):
    if response.user.is_authenticated:
        video_file = VisionGalleryFiles.objects.filter(user=response.user, file_category='video').first()

        return render(response, 'user_files/watch_video.html', {'video_file': video_file})
    else:
        return redirect('accounts:sign_in_to_members_area')


def processing_video(response):
    if response.user.is_authenticated:
        return render(response, 'user_files/processing_video.html', {})
    else:
        return redirect('accounts:sign_in_to_members_area')