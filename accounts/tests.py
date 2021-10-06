from django.test import TestCase
from django.urls import reverse
from .models import Users, Profile


def create_user(email, phone, password):
    return Users.objects.create(email=email, phone_number=phone, password=password)


# Create your tests here.
class AllAccountUrlsTest(TestCase):
    def test_login_url(self):
        """dont forget to use saved email and passwords so it redirects to the right place"""
        response = self.client.post(reverse("users:login_user", ),
                                    data={'password': 'inbfuhisd2345', 'email': 'e@g.com'})
        self.assertEqual(response.status_code, 302)

    def test_register_url(self):
        response = self.client.post(reverse("users:register_user", ), data={'phone': '123456789', 'email': 'i@gm.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/add-payment")

    def test_forgot_password_url(self):
        response = self.client.post(reverse("users:forgot_password_send_email", ), data={'email': 'i@gm.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/forgot-password")


class UserDatabaseTests(TestCase):
    def test_changes_the_token(self):
        user = create_user('i@g.com', '+1234567890', 'yugbskf7380')
        profile = Profile(user=user, customer_id='sfgrid')
        old_token = profile.user_token
        profile.change_token()
        new_token = profile.user_token
        self.assertNotEqual(new_token, old_token)
