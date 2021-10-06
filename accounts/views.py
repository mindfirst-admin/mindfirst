from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .models import Profile
from .extras_ import *
from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()


# Create your views here.
def register_user(request):
    email = request.POST['email']
    phone = request.POST['phone']
    agreed = request.POST['agreed']

    if User.objects.filter(email=email).count() != 0:
        messages.error(request, 'Email already in use')
        return HttpResponseRedirect(reverse('main:sign_up'))

    if not email or not phone or not agreed:
        messages.error(request, 'All input fields need to be appropriately filled')
        return HttpResponseRedirect(reverse('main:sign_up'))

    if '+' in phone:
        phone = phone.replace('+', '')

    request.session['user_registration'] = {
        'email': email,
        'phone': phone
    }

    return HttpResponseRedirect(reverse('main:add_payment'))


def login_user(request):
    password = request.POST['password']
    email = request.POST['email']

    if User.objects.filter(email=email).count() == 0:
        messages.error(request, 'Email doesn\'t exist')
        return HttpResponseRedirect(reverse('main:login'))

    user = auth.authenticate(email=email, password=password)
    if user is not None:
        user_profile = Profile.objects.get(user=user)
        if user_profile.is_subscribed:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:members_area'))
        else:
            messages.error(request, 'You are not on a subscription plan')
            return HttpResponseRedirect(reverse('main:login'))

    messages.error(request, 'Incorrect email or password')
    return redirect('main:login')


def forgot_password_send_email(request):
    email = request.POST['email']
    user = User.objects.filter(email=email).first()

    if user is not None:
        request.session['email'] = email
        return redirect('api:new_password')

    messages.error(request, 'Email doesn\'t exist')
    return HttpResponseRedirect(reverse('main:forgot_password'))
