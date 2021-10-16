from django.db import models


# Create your models here.
class UserPurchases(models.Model):
    purchase = models.CharField(max_length=255, default='')
    stripe_customer_id = models.CharField(max_length=255, default='')
    stripe_checkout_id = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='')
    date_paid = models.DateTimeField(auto_now_add=True)
