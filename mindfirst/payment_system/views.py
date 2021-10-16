import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import UserPurchases

stripe.api_key = settings.STRIPE_API_KEY


# Create your views here.
def payment_pages(response, product):
    if product == 'book':
        return render(response, 'payments/book_payment.html', {})

    elif product == 'workbook':
        return render(response, 'payments/workbook_payment.html', {})

    elif product == 'membership':
        return render(response, 'payments/membership_payment.html', {})


def membership_monthly(request):
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payment/thank-you',
        cancel_url='http://127.0.0.1:8000/payment/thank-you',
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price': 'price_1Jjn2uGjOqEuQIlnJY2BXS0I',
            'quantity': 1
        }],
    )
    request.session['stripe_payment'] = 'monthly_membership'
    request.session['session_id'] = session.id
    print(session)
    if session:
        return redirect(session.url, code=302)

    messages.error(request, 'An error occurred, please try again')
    return redirect('payments:payment_pages', product='membership')


def membership_annually(request):
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payment/thank-you',
        cancel_url='http://127.0.0.1:8000/payment/payment-unsuccessful',
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price': 'price_1JCoJ7GjOqEuQIlnR7tC51sB',
            'quantity': 1
        }],
    )
    request.session['stripe_payment'] = 'annual_membership'
    request.session['session_id'] = session.id
    if session:
        return redirect(session.url, code=302)

    messages.error(request, 'An error occurred, please try again')
    return redirect('payments:payment_pages', product='membership')


def ebook_purchase(request):
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payment/thank-you',
        cancel_url='http://127.0.0.1:8000/payment/payment-unsuccessful',
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price': 'price_1Jjmx2GjOqEuQIlnMOgaTifz',
            'quantity': 1
        }],
    )
    request.session['stripe_payment'] = 'ebook'
    request.session['session_id'] = session.id
    if session:
        return redirect(session.url, code=302)

    messages.error(request, 'An error occurred, please try again')
    return redirect('payments:payment_pages', product='book')


def audiobook_purchase(request):
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payment/thank-you',
        cancel_url='http://127.0.0.1:8000/payment/payment-unsuccessful',
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price': 'price_1JjmzcGjOqEuQIlnfm1W6YsY',
            'quantity': 1
        }],
    )
    request.session['stripe_payment'] = 'audiobook'
    request.session['session_id'] = session.id
    if session:
        return redirect(session.url, code=302)

    messages.error(request, 'An error occurred, please try again')
    return redirect('payments:payment_pages', product='book')


def audiobook_n_ebook_purchase(request):
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payment/thank-you',
        cancel_url='http://127.0.0.1:8000/payment/payment-unsuccessful',
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price': 'price_1Jjn0mGjOqEuQIlnp1YMVrEu',
            'quantity': 1
        }],
    )
    request.session['stripe_payment'] = 'audiobook_x_ebook'
    request.session['session_id'] = session.id
    if session:
        return redirect(session.url, code=302)

    messages.error(request, 'An error occurred, please try again')
    return redirect('payments:payment_pages', product='book')


def workbook_purchase(request):
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payment/thank-you',
        cancel_url='http://127.0.0.1:8000/payment/payment-unsuccessful',
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price': 'price_1JjmvHGjOqEuQIlnjf3D5Fm3',
            'quantity': 1
        }],
    )
    request.session['stripe_payment'] = 'workbook'
    request.session['session_id'] = session.id
    if session:
        return redirect(session.url, code=302)

    messages.error(request, 'An error occurred, please try again')
    return redirect('payments:payment_pages', product='workbook')


def thank_you(request):
    purchase = request.session['stripe_payment']
    retrieved_session = stripe.checkout.Session.retrieve(
        request.session['session_id'],
    )

    if retrieved_session.payment_status != 'unpaid':
        customer_id = retrieved_session.customer
        email = retrieved_session.customer_details.email

        new_purchase = UserPurchases(purchase=purchase, stripe_customer_id=customer_id,
                                     stripe_checkout_id=retrieved_session.id, email=email)
        new_purchase.save()
    return render(request, 'payments/thank_you.html')


def payment_unsuccessful(request):
    request.session['stripe_payment'] = ''
    request.session['session_id'] = ''
    return render(request, 'payments/payment_unsuccessful.html')
