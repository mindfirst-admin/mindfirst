from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
import string
import random


def generate_user_token():
    length = 36
    small_letters = string.ascii_lowercase
    numbers = string.digits
    code_ = small_letters + numbers

    while True:
        token = ''.join(random.choices(code_, k=length))  # generates random code for alphabets
        if Profile.objects.filter(user_token=token).count() == 0:
            break

    return token


def create_password():
    length = 16
    small_letters = string.ascii_lowercase
    numbers = string.digits
    p_wrd_list = small_letters + numbers

    while True:
        p_wrd = ''.join(random.choices(p_wrd_list, k=length))
        if Users.objects.filter(password=p_wrd).count() == 0:
            break

    return p_wrd


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, phone_number=None, is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError("All the fields haven't been adequately filled")
        if not password:
            raise ValueError("All the fields haven't been adequately filled - password")

        user_obj = self.model(
            email=self.normalize_email(email),
        )

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.phone_number = phone_number
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, password=None, phone_number=None):
        user = self.create_user(
            email,
            password=password,
            phone_number=phone_number,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, phone_number=None):
        user = self.create_user(
            email,
            password=password,
            phone_number=phone_number,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# Create your user models here.
class Users(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.IntegerField()

    # django defaults
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    # django default functions
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    user_token = models.CharField(max_length=36, default=generate_user_token)
    aspiration_name = models.CharField(max_length=255, default="Aspiration")
    is_subscribed = models.BooleanField(null=False, default=False)
    customer_id = models.CharField(max_length=50, default='')

    scaled_habits = models.IntegerField(default=0)
    yellow_habits = models.IntegerField(default=0)
    red_habits = models.IntegerField(default=0)
    green_habits = models.IntegerField(default=0)

    negative_behaviors_done_this_week = models.CharField(max_length=10, default='0/0')
    positive_behaviors_done_this_week = models.CharField(max_length=10, default='0/0')

    all_positive_habits_this_week = models.CharField(max_length=20, default='[]')
    all_scaled_habits_this_week = models.CharField(max_length=20, default='[]')
    all_negative_habits_this_week = models.CharField(max_length=20, default='[]')

    all_positive_habits_in_twelve_weeks = models.CharField(max_length=40, default='[]')
    all_scaled_habits_in_twelve_weeks = models.CharField(max_length=40, default='[]')
    all_negative_habits_in_twelve_weeks = models.CharField(max_length=40, default='[]')

    def change_token(self):
        self.user_token = generate_user_token()

    def __str__(self):
        return self.user.email


class FiveDayWaitingList(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, unique=True)
    last_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.email


class MembershipWaitingList(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, unique=True)
    last_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.email
