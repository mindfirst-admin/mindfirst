from django.shortcuts import render, redirect

from accounts.models import Profile
from behaviours.models import LimitingBeliefs, BehaviourMapping
from files_gallery.models import VisionGalleryFiles


# Create your views here.
def homepage(request):
    return render(request, 'main/homepage.html')


def our_products(request):
    return render(request, 'main/products.html')


def product_details(request, product):
    if product == '5-day-challenge':
        main_header = '5-Day Challenge'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        p1 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. ' \
             'Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p2 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p3 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        link = '/accounts/5-day-challenge'
        image = 'main/assets/landing_image.jpg'

    elif product == 'book':
        main_header = 'Progress Equals Happiness'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        p1 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p2 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p3 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        link = '/payment/~book'
        image = 'main/assets/landing_image.jpg'

    elif product == 'workbook':
        main_header = 'Our Workbook'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        p1 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p2 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p3 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        link = '/payment/~workbook'
        image = 'main/assets/landing_image.jpg'

    elif product == 'membership':
        main_header = 'Mind First Membership'
        sub_header = 'Repeatable, Practical, Proven, Peer-Reviewed Science'
        p1 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p2 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        p3 = 'From cradle to the grave, your brain will process more events than there are stars in our universe. ' \
             'As your body’s “central processing unit,” your brain is in charge of a staggering array of functions,' \
             ' from processing and perceiving stimuli to motor control and memory storage. Habits and beliefs progr' \
             'ammed into your mind over a lifetime of responding to experiences are stored in long-term memory, ' \
             'and may cause you to resist new ways of doing things.'
        link = '/payment/~membership'
        image = 'main/assets/landing_image.jpg'

    else:
        return render(request, 'main/404.html')

    return render(request, 'main/product_details.html', {
        'main_header': main_header,
        'sub_header': sub_header,
        'p1': p1,
        'p2': p2,
        'p3': p3,
        'image': image,
        'link': link,
    })


def members_area(request):
    if request.user.is_authenticated:
        aspiration_files = VisionGalleryFiles.objects.filter(user=request.user, file_category='aspirations').first()
        video_file = VisionGalleryFiles.objects.filter(user=request.user, file_category='video').first()
        profile = Profile.objects.get(user=request.user)

        if not aspiration_files:
            aspiration_image = 'main/assets/landing_image.jpg'
        else:
            # add file
            aspiration_image = 'media/' + str(aspiration_files)

        if not video_file:
            has_video = False
        else:
            has_video = True

        aspiration_name = profile.aspiration_name
        behaviours_list = BehaviourMapping.objects.filter(user=request.user, is_selected=True).all()

        content = {
            'vision_gallery_video': video_file,
            'has_video': has_video,
            'profile': profile,
            'aspiration_image': aspiration_image,
            'aspiration_name': aspiration_name,
            'behaviours_list': behaviours_list,
        }
        return render(request, 'main/members_area.html', content)

    return redirect('accounts:sign_in_to_members_area')


def limiting_beliefs(request):
    if request.user.is_authenticated:
        beliefs = LimitingBeliefs.objects.filter(user=request.user).first()
        if beliefs is not None:
            data = beliefs.beliefs
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
        return render(request, 'main/limiting_beliefs.html', {'data': data})

    return redirect('accounts:sign_in_to_members_area')
