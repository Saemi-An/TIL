from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="index"),
    path("cart", views.cart, name="cart"),
    path("cart/delete_item/<int:item_id>", views.delete_cart_item, name="delete_cart_item"),
    path("register", views.register),
    path("register-completed", views.register_completed),
]
