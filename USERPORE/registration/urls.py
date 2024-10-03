from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="index"),
    path("cart", views.cart, name="cart"),
    path("register", views.register),
    path("register-completed", views.register_completed),
]
