from django.urls import path

from . import views

urlpatterns = [
    path("", views.review),   # 폼뷰 - 함수 뷰
    path("review2", views.review2),   # 폼뷰 - 리퓨폼으로 유효성검사 간단히
    # path("review2", views.ReviewView.as_view()),   # 클래스 뷰 / 폼 뷰 / create 뷰
    path("thank-you", views.thank_you),
    # path("thank-you", views.ThankYouView.as_view()),   # Class View - Template View
    path("review-list", views.ReviewListView.as_view()),   # Class View - TemplateView & ListView
    path("review-detail/<str:user_name>", views.ReviewDetailView.as_view()),   # Class View - TemplateView & ListView
    # path("review-detail/<int:pk>", views.ReviewDetailView.as_view()),   # Class View - TemplateView & ListView
]