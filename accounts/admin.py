from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(Profile)
admin.site.register(FiveDayWaitingList)
admin.site.register(MembershipWaitingList)
