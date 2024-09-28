from django.urls import path

from . import views

urlpatterns = [
    path("", views.starting_page, name="starting_page"),
    path("posts/", views.posts, name="posts-page"),
    path("posts/<slug:slug>", views.post_detail, name="post-detail-page"),   # slug : SEO friednly identifier (그냥 int보다 낫다) / 텍스트와 대쉬만 갖는 형식(- 이외 특수문자 X)
    
    path("db_index", views.db_index, name="db_index"),
    path("db_posts", views.db_posts, name="db_posts"),
    path("db_detail/<slug:slug>", views.db_detail, name="db_detail"),
    path("db_detail/<str:name>/<str:email>", views.author_email, name="author_email"),
]