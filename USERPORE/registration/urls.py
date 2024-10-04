from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="index"),
    path("cart", views.cart, name="cart"),
    path("cart/delete_cart_item", views.delete_cart_item, name="delete_cart_item"),   # 장바구니 상품 삭제
    path("cart/increase_quantity", views.increase_quantity, name="increase_quantity"),   # 장바구니 수량 +
    path("cart/decrease_quantity", views.decrease_quantity, name="decrease_quantity"),   # 장바구니 수량 -
    path("register", views.register),
    path("register-completed", views.register_completed),
]
