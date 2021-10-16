import json

from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


# Create your views here.
def reserve_membership_spot(request):
    if request.POST.get('data', None):
        data = json.loads(request.POST.get('data'))

        new_waiting_member = MembershipWaitingList(email=data['email'], first_name=data['firstname'],
                                                   last_name=data['lastname'])
        new_waiting_member.save()
        return JsonResponse('Done', safe=False)
    return render(request, 'accounts/reserve_membership_spot.html')


def reserve_fd_challenge_spot(request):
    if request.POST.get('data', None):
        data = json.loads(request.POST.get('data'))

        new_waiting_member = FiveDayWaitingList(email=data['email'], first_name=data['firstname'],
                                                last_name=data['lastname'])
        new_waiting_member.save()
        return JsonResponse('Done', safe=False)
    return render(request, 'accounts/reserve_fd_challenge_spot.html')


def sign_in_to_members_area(request):
    if request.POST:
        password = request.POST['password']
        email = request.POST['email']


        # user = User.objects.filter(email='email@gmail.com').first()
        # user.set_password('iaminnathemale')
        # user.save()

        if User.objects.filter(email=email).count() == 0:
            messages.error(request, 'Email doesn\'t exist in our database')

        else:
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                user_profile = Profile.objects.filter(user=user).first()
                if user_profile:
                    if user_profile.is_subscribed and user.is_active:
                        auth.login(request, user)
                        return HttpResponseRedirect(reverse('main:members_area'))
                messages.error(request,
                               'You are not on a membership subscription plan or your account is disabled')
            else:
                messages.error(request, 'Incorrect email or password')

    return render(request, 'accounts/sign_in_to_members_area.html')


def user_forgot_password(request):
    if request.POST:
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user is not None:
            password = create_password()
            user.set_password(password)
            user.save()

            user_auth = auth.authenticate(email=email, password=password)

            if user_auth:
                # send email via active campaign
                messages.error(request,
                               'Your password was changed successfully, an email has been sent with the new details')
            else:
                messages.error(request, 'There was an error changing your password, please try again')
        else:
            messages.error(request, 'Email doesn\'t exist')

    return render(request, 'accounts/forgot_password.html')


def logout(request):
    auth.logout(request)
    return redirect('main:homepage')
