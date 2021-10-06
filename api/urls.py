from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("create-checkout-session-monthly", views.create_checkout_session_monthly, name="monthly_checkout"),
    path("create-checkout-session-yearly", views.create_checkout_session_yearly, name="yearly_checkout"),
    path("payment-successful", views.payment_successful, name="payment_successful"),
    path("payment-unsuccessful", views.payment_unsuccessful, name="payment_failed"),
    path("new-password", views.new_password, name='new_password'),
]
