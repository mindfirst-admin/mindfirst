from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()


# Create your models here.
class Subscription(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    package_plan_id = models.CharField(max_length=21, default='')
    subscription_cancel_date = models.DateField(blank=True, null=True)
    subscription_start_date = models.DateField(auto_now_add=True)
    subscription_id = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.package_plan_id
