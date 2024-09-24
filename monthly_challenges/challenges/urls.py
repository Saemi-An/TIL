from django.urls import path

# urls.py 파일이 있는 있는 곳과 동일한 위치에서 views를 가져온다
from . import views


urlpatterns = [
    path("", views.index),
    path("<int:month>", views.monthly_challenge_by_number),
    path("<str:month>", views.monthly_challenge, name="url_name"),   # url path에 이름을 부여함 
]