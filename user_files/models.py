from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.user.id, instance.file_category, filename)


# Create your models here.
class UserFiles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    file_category = models.CharField(max_length=20)  # either aspirations, values or gallery_video
