from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('~<str:product>/', views.payment_pages, name="payment_pages"),

    path('membership_monthly/', views.membership_monthly, name="membership_monthly"),

    path('membership_annually/', views.membership_annually, name="membership_annually"),

    path('ebook_purchase/', views.ebook_purchase, name="ebook_purchase"),

    path('audiobook_purchase/', views.audiobook_purchase, name="audiobook_purchase"),

    path('audiobook_n_ebook_purchase/', views.audiobook_n_ebook_purchase, name="audiobook_n_ebook_purchase"),

    path('workbook_purchase/', views.workbook_purchase, name="workbook_purchase"),

    path('payment-unsuccessful/', views.payment_unsuccessful, name="payment_unsuccessful"),

    path('thank-you/', views.thank_you, name="thank_you"),
]