from django.urls import path
from . import views, forms

app_name = 'gallery'

urlpatterns = [
    path("", views.vision_gallery, name="vision_gallery"),

    path("edit-aspirations/", views.edit_aspirations, name="edit_aspirations"),

    path("edit-values/", views.edit_values, name="edit_values"),

    path("processing-video/", views.processing_video, name="processing_video"),

    path("watch-video/", views.watch_video, name="watch_video"),

    # form
    path("delete-file/", forms.delete_file, name="delete_file"),

    path("upload-files/", forms.upload_files, name="upload_files"),

    path("process-files", forms.process_video, name="process_video"),

    path("add-to-values", forms.add_to_values, name="add_to_values"),
]

