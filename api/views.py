# this page will handle the payment and other views to avoid complication

import random
import string
import stripe
import os
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages, auth
from accounts.extras_ import *
from user_files.models import UserFiles
from .models import Subscription

User = get_user_model()
stripe.api_key = settings.STRIPE_API_KEY


def create_password():
    length = 16
    small_letters = string.ascii_lowercase
    numbers = string.digits
    p_wrd_list = small_letters + numbers

    while True:
        p_wrd = ''.join(random.choices(p_wrd_list, k=length))
        if User.objects.filter(password=p_wrd).count() == 0:
            break

    return p_wrd


def create_checkout_session_monthly(request):
    # details
    user = request.session['user_registration']

    if user:
        # creating a customer
        customer = stripe.Customer.create(
            description="New customer",
            email=user['email'],
            phone=user['phone'],
        )
        if customer:
            # actual payment
            session = stripe.checkout.Session.create(
                customer=customer.id,
                success_url='http://127.0.0.1:8000/payment/payment-successful',
                cancel_url='http://127.0.0.1:8000/payment/payment-successful',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[{
                    'price': 'price_1JBRV4GjOqEuQIlnuUIcvrnI',
                    'quantity': 1
                }],
                discounts=[{
                    'coupon': '1',
                }],
            )
            request.session['customer'] = {
                'cid': customer.id,
                'plan': 'monthly',
                'sid': session.id
            }
            return redirect(session.url, code=302)

    return HttpResponseRedirect(reverse('main:sign_up'))


def create_checkout_session_yearly(request):
    # details
    user = request.session['user_registration']

    if user:
        # creating a customer
        customer = stripe.Customer.create(
            description="New customer",
            email=user['email'],
            phone=user['phone'],
        )
        if customer:
            # actual payment
            session = stripe.checkout.Session.create(
                customer=customer.id,
                success_url='http://127.0.0.1:8000/payment/payment-successful',
                cancel_url='http://127.0.0.1:8000/payment/payment-unsuccessful',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[{
                    'price': 'price_1JCoJ7GjOqEuQIlnR7tC51sB',
                    'quantity': 1
                }],
                discounts=[{
                    'coupon': '2',
                }],
            )
            request.session['customer'] = {
                'cid': customer.id,
                'plan': 'yearly',
                'sid': session.id
            }
            return redirect(session.url, code=302)
    return HttpResponseRedirect(reverse('main:sign_up'))


def payment_successful(request):
    sign_up_details = request.session['user_registration']
    customer_details = request.session['customer']
    email = sign_up_details['email']
    phone_number = sign_up_details['phone']

    customer_id = customer_details['cid']
    plan_id = customer_details['plan']
    sub_id = customer_details['sid']

    password = create_password()

    # sign-in user
    new_user = User(email=email, phone_number=phone_number)
    new_user.set_password(password)
    new_user.save()

    # profile db creation
    new_user_profile = Profile(user=new_user, customer_id=customer_id, is_subscribed=True)
    new_user_profile.save()

    # subscription db creation
    new_subscription = Subscription(user=new_user, package_plan_id=plan_id, subscription_id=sub_id)
    new_subscription.save()

    request.session['new_profile'] = {
        'email': email,
        'password': password
    }

    return HttpResponseRedirect(reverse('main:payment_success'))


def payment_unsuccessful(request):
    for key in request.session.keys():
        del request.session[key]
    return HttpResponseRedirect(reverse('main:payment_failed'))


def new_password(request):
    password = create_password()
    print(password)
    email = request.session['email']

    user = User.objects.get(email=email)
    if user:
        user.set_password(password)
        user.save()

        user_auth = auth.authenticate(email=email, password=password)

        if user_auth:
            send_password_changed_mail(user)
            send_password_mail(password, email)
            return HttpResponseRedirect(reverse('main:forgot_password'))

        messages.error(request, 'There was an error changing your password, please try again')
        return HttpResponseRedirect(reverse('main:forgot_password'))

    messages.error(request, 'Email does not exist')
    return HttpResponseRedirect(reverse('main:forgot_password'))

