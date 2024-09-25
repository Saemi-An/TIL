from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),   # index를 위한 url & url_name 추가
    path("posts/", views.posts, name="posts"),
    path("posts/<int:post_num>", views.post_detail),
]