import os
import random
import string

import cv2 as cv
import numpy as np
from django.conf import settings
from django.core.files.base import File
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import UserFiles


def generate_random_path():
    length = 12
    small_letters = string.ascii_lowercase
    numbers = string.digits
    code_ = small_letters + numbers
    random_number = ''.join(random.choices(code_, k=length))
    return random_number


# Create your views here.
def delete_file(request):
    file_names = request.POST
    for file_name in file_names:
        if file_name != 'csrfmiddlewaretoken':
            file_name = file_name.replace('media/', '')
            path = UserFiles.objects.get(user=request.user, file=file_name)
            if path:
                path.delete()
                os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
    return HttpResponseRedirect(reverse('main:edit_aspirations'))


def add_to_values(request):
    file_names = request.POST

    if file_names:
        all_files = UserFiles.objects.filter(user=request.user, file_category="values").all()
        if all_files:
            for file in all_files:
                file = file.file
                os.remove(os.path.join(settings.MEDIA_ROOT, str(file)))
        all_files.delete()

        for name in file_names:
            if name != 'csrfmiddlewaretoken':
                admin_file = f'{settings.MEDIA_REL_PATH}{name}'
                with open(admin_file, 'rb') as f:
                    new_file = UserFiles(user=request.user, file=File(f, name=admin_file.split('\\')[-1]),
                                         file_category="values")
                    new_file.save()
    return HttpResponseRedirect(reverse('main:vision_gallery'))


@csrf_exempt
def process_video(request):
    # main variables
    resolution = (500, 500)
    _ = cv.VideoWriter_fourcc(*'vp80')  # webm file
    rate = 40
    image_dimensions = (500, 500)

    # get files
    aspirations = str(UserFiles.objects.filter(user=request.user, file_category='aspirations').first().file)
    values = [str(i.file) for i in UserFiles.objects.filter(user=request.user, file_category='values').all()]
    values.insert(0, aspirations)

    image_video_files = values

    to_begin = request.POST['begin']
    if to_begin:
        # remove all the files in the directory
        all_files = UserFiles.objects.filter(user=request.user, file_category="video").all()
        if all_files:
            for file in all_files:
                file = file.file
                os.remove(os.path.join(settings.MEDIA_ROOT, str(file)))
        all_files.delete()

        # create output video path and name
        video_path = f'{settings.MEDIA_REL_PATH}start_video_{generate_random_path()}.webm'
        output_video = cv.VideoWriter(video_path, _, rate, resolution)

        # run loop
        prev_image = np.zeros((500, 500, 3), np.uint8)
        for file in image_video_files:
            file_path = settings.MEDIA_ROOT + '/' + file
            image = cv.imread(file_path)
            image = cv.resize(image, image_dimensions, interpolation=cv.INTER_AREA)

            for i in range(101):
                alpha = i / 100
                beta = 1.0 - alpha
                dst = image
                try:
                    dst = cv.addWeighted(image, alpha, prev_image, beta, 0.0)
                except Exception as e:
                    print(e)
                finally:
                    if i == 100:
                        for j in range(150):
                            output_video.write(dst)

                output_video.write(dst)
                if cv.waitKey(1) == ord('q'):
                    return

            prev_image = image

            if cv.waitKey(5000) == ord('q'):
                return

        output_video.release()

        # save video
        video = video_path.replace(settings.MEDIA_REL_PATH, '')
        with open(video_path, 'rb') as f:
            new_video = UserFiles(user=request.user, file=File(f, name=video),
                                  file_category="video")
            new_video.save()

        """Todo: fix the remove file from other dir after save"""
        os.remove(os.path.join(settings.MEDIA_ROOT, video))

        # return Response
        return JsonResponse('done', safe=False)
    return JsonResponse('', safe=False)


def upload_files(request):
    file = request.FILES['aspirations_upload']
    if file:
        new_file = UserFiles(user=request.user, file=file, file_category="aspirations")
        new_file.save()
    return HttpResponseRedirect(reverse('main:edit_aspirations'))
