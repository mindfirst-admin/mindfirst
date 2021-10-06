from django.db import models
from accounts.models import Users


# Create your models here.
class DayModel(models.Model):
    day_id = models.IntegerField(default=0)
    title = models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='admin/days/video_images')
    description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return self.title


class FiveDayModel(models.Model):
    day_id = models.IntegerField(default=0)
    title = models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='admin/5days/video_images')
    description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return self.title


class WeekModel(models.Model):
    week_id = models.IntegerField(default=0)
    title = models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='admin/weeks/video_images')
    description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return self.title


class MindWorkshopModel(models.Model):
    week_id = models.IntegerField(default=0)
    title = models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='admin/mind_workshop/video_images')
    description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return self.title


class FolderModel(models.Model):
    day = models.ForeignKey(DayModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    five_day = models.ForeignKey(FiveDayModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    week = models.ForeignKey(WeekModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    mind_workshop = models.ForeignKey(MindWorkshopModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    file = models.FileField(upload_to='admin/data/folder')
    file_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.file_name


class WhatYoullLearnModel(models.Model):
    day = models.ForeignKey(DayModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    five_day = models.ForeignKey(FiveDayModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    week = models.ForeignKey(WeekModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    mind_workshop = models.ForeignKey(MindWorkshopModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    image = models.FileField(upload_to='admin/what_you\'ll_learn/', blank=True, null=True)
    video = models.FileField(upload_to='admin/what_you\'ll_learn/', blank=True, null=True)
    text = models.CharField(max_length=1024, default='', blank=True, null=True)
