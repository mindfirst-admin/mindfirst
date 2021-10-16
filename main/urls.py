from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("products", views.our_products, name="our_products"),

    path("members-area", views.members_area, name="members_area"),

    path("limiting-beliefs/", views.limiting_beliefs, name="limiting_beliefs"),

    path("product-details/<str:product>", views.product_details, name="product_details"),
]

