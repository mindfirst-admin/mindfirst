from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Profile


def send_welcome_email(email):
    profile_email = email

    template = render_to_string('accounts/welcome_template.html', {})

    email = EmailMessage(
        'Thanks for signing up',
        template,
        settings.EMAIL_HOST_USER,
        [profile_email, ]
    )
    email.fail_silently = False
    email.send()


def send_verification_email(user_profile):
    token = user_profile.user_token
    domain = 'the-domain-name'
    link = f'{domain}/verify-user/{token}'
    profile_email = user_profile.user.email

    template = render_to_string('accounts/verification_mail.html', {'link': link})

    email = EmailMessage(
        'Verify your email',
        template,
        settings.EMAIL_HOST_USER,
        [profile_email, ]
    )
    email.fail_silently = False
    email.send()


def send_forgot_password_mail(user):
    user_email = user.email
    profile = Profile.objects.filter(user=user).first()
    token = profile.user_token
    print(token)
    domain = 'the-domain-name'
    link = f'{domain}/verify-forgot-password/{token}'

    template = render_to_string('accounts/forgot_password.html', {'link': link})

    email = EmailMessage(
        'Reset your password',
        template,
        settings.EMAIL_HOST_USER,
        [user_email, ]
    )
    email.fail_silently = False
    email.send()


def send_password_changed_mail(user):
    profile_email = user.email

    template = 'Password has been changed'

    email = EmailMessage(
        'Password changed',
        template,
        settings.EMAIL_HOST_USER,
        [profile_email, ]
    )
    email.fail_silently = False
    email.send()


def send_password_mail(password, email):
    template = 'Password has been changed'

    email = EmailMessage(
        f'Your password is {password}, email is {email}',
        template,
        settings.EMAIL_HOST_USER,
        [email, ]
    )
    email.fail_silently = False
    email.send()
