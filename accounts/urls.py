from django.urls import path
from. import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_user, name="login_user"),

    path("register/", views.register_user, name="register_user"),

    path("forgot-send-mail/", views.forgot_password_send_email, name="forgot_password_send_email"),
]
