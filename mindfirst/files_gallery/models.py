from django.db import models
from accounts.models import Users


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.user.id, instance.file_category, filename)


def admin_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/admin/<filename>
    return 'admin/{0}'.format(filename)


class VisionGalleryFiles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    file_category = models.CharField(max_length=20)  # either 'aspirations', 'values' or 'video'


class AdminValuesImages(models.Model):
    image = models.FileField(upload_to=admin_directory_path)
