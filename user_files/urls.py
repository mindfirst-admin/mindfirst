from django.urls import path
from . import views

app_name = "user_files"

urlpatterns = [
    path("delete-files", views.delete_file, name="delete_file"),
    path("upload-files", views.upload_files, name="upload_files"),
    path("process-files", views.process_video, name="process_video"),

    path("add-values", views.add_to_values, name="add_to_values"),
]
