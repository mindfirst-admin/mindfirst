from django.db import models
from accounts.models import Users
from django.shortcuts import get_object_or_404


# Create your models here.
class BehaviourMaps(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=1024, default='', blank=True, null=True)
    behavior_value = models.CharField(max_length=3, default='+ve')
    impact = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    is_scaled = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    done_today = models.BooleanField(default=False)
    thumb_up_clicked = models.IntegerField(default=0)
    thumb_down_clicked = models.IntegerField(default=0)
    thumb_up_week = models.IntegerField(default=0)
    thumb_down_week = models.IntegerField(default=0)


class GoodHabitDesign(models.Model):
    behavior = models.OneToOneField(BehaviourMaps, on_delete=models.CASCADE)
    after_or_before = models.CharField(max_length=255, default='')
    act = models.CharField(max_length=255, default='')
    celebrate = models.CharField(max_length=255, default='')
    frequency = models.CharField(max_length=255, default='')
    number_of_times = models.CharField(max_length=2, default=0)


class BadHabitDesign(models.Model):
    behavior = models.OneToOneField(BehaviourMaps, on_delete=models.CASCADE)
    trigger = models.CharField(max_length=255, default='')
    make_less_obvious = models.CharField(max_length=255, default='')
    make_harder = models.CharField(max_length=255, default='')
    frequency = models.CharField(max_length=255, default='')
    number_of_times = models.CharField(max_length=2, default=0)


class LimitingBeliefs(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    beliefs = models.CharField(max_length=10000)