from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic.edit import CreateView

from .forms import ReviewForm
from .models import Review


# [리뷰폼]1단계 - 함수 뷰
def review(request):
    if request.method == "POST":
        entered_username = request.POST["username"]

        if entered_username == "" and len(entered_username) <= 10:   # 수동 validation
            return render(request, "reviews/review.html", {
                "has_error" : True,
            })
    
        print(f"POST 요청으로 입력된 데이터: {entered_username}")

        return HttpResponseRedirect("/thank-you")

    return render(request, "reviews/review.html")

# ***[리뷰폼]2단계 - 리뷰폼(forms.py)을 사용하여 자동 validation
def review2(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)   # 유저가 입력한 데이터를 POST로 받은 뒤 --> 그 데이터를 ReviewForm() 안에 넣어줌 (To populate the form with the submitted data)
        
        # existing_data = get_object_or_404(Review, pk=1)   # Review 테이블에서 pk=1인 쿼리셋 가져오기
        # form = ReviewForm(request.POST, instance=existing_data)   # POST 요청이 들어오면 / 요청된 POST 데이터를 exising_data에 업데이트 하기

        if form.is_valid():   # is_valid() - Django form 클래스의 유효성 검사용 빌트인 함수(required가 디폴트임)
            print(form.cleaned_data)   # 유효성 검사를 통과한 데이터가 채워짐 - cleaned_data
            # review = Review(   # DB Review 테이블에 저장: 컬럼명 = form.cleaned_data["키값"] / 컬럼명  != 키값 가능
            #     user_name = form.cleaned_data["user_name"],
            #     user_email = form.cleaned_data["user_email"],
            #     review_text = form.cleaned_data["review_text"],
            #     rating = form.cleaned_data["rating"],)
            # review.save()
            
            # ModelForm 사용시 DB에 저장할 값들을 일일이 DB 컬럼명과 맞춰주지 않아도 됨
            form.save()

            return HttpResponseRedirect("/thank-you")
    else:
        form = ReviewForm()

    return render(request, "reviews/review2.html", {
        "form" : form,
    })

# [리뷰폼]3단계 - 클래스 뷰
# class ReviewView(View):
#     def get(self, request):   # 모두 소문자
#         form = ReviewForm()

#         return render(request, "reviews/review2.html", { "form" : form })

#     def post(self, request):   # 모두 소문자
#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             form.save()

#             return HttpResponseRedirect("/thank-you")
        
#         return render(request, "reviews/review2.html", { "form" : form })

# [리뷰폼]4단계 - 폼 뷰
# class ReviewView(FormView):
#     form_class = ReviewForm
#     template_name = "reviews/review2.html"   # 여기까지 GET req는 다 커버됨
#     success_url = "/thank-you"   # POST req가 is_valid 데이터와 함께 갈 url을 지정해줌

#     # valid input이 POST 되었을 때 장고가 실행할 함수: (데이터 저장)
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
    
# [리뷰폼]5단계 - create 뷰
# class ReviewView(CreateView):
#     model = Review
#     form_class = ReviewForm
#     template_name = "reviews/review2.html"
#     success_url = "/thank-you"





def thank_you(request):
    return render(request, "reviews/thank_you.html")

# Class-Based View: Template View
# 2단계 : 단순 클래스화
# class ThankYouView(View):
#     def get(self, request):
#         return render(request, "reviews/thank_you.html")
    
# 3단계: 템플렛 뷰: 특정 url로 GET요청이 오면 아래의 템플렛을 렌더링해서 응답으로 보내준다 + context
# class ThankYouView(TemplateView):
#     template_name = "reviews/thank_you.html"   # template_name (**TemplateView 클래스의 속성명)
#         # get(self, request) 함수, render(request, "html 파일명") 함수가 필요하지 않음
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["message"] = "This Works!"
        
#         return context





# [전체리뷰목록]1단계 : 템플렛 뷰 
class ReviewListView(TemplateView):
    template_name = "reviews/review_list.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.all()
        # reviews = get_object_or_404(Review, all)   # --> 불가능. get_object_or_404()는 특정 객체를 검색할 때 사용된다.
        context["reviews"] = reviews

        return context

# [전체리뷰목록]2단계 : 리스트 뷰
# class ReviewListView(ListView):
#     template_name = "reviews/review_list.html"
#     model = Review
#     context_object_name = "reviews"   # 이 설정 없이는 html에서 for문 돌릴 때 키로"object_list"라는 이름을 사용해야함
    
    # 특정 조건(예: 별점 4점 이상)의 데이터 목록만을 취하고 싶을 때 사용 // 주석처리하면 모든 리뷰 볼 수 잇음
    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     filtered_list_data = base_query.filter(rating__gte=4)
    #     return filtered_list_data
    



# [리뷰상세]1단계 : 템플렛 뷰 
class ReviewDetailView(TemplateView):
    template_name = "reviews/review_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = kwargs["user_name"]
        detail = Review.objects.filter(user_name=user_name)
        context["detail"] = detail
        context["user_name"] = user_name

        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context
    
# [리뷰상세]2단계 : 리스트 뷰 --> ????
# returning a template for a GET req for about A SINGLE PIECE OF DATA
# class ReviewDetail2View(DetailVeiw):
#     template_name = "reviews/review_detail2.html"
#     model = Review
    # 소문자 테이블명(모델명)을 변수명으로 context에 자동으로 전달됨

class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        # fav_review = Review.objects.get(pk=review_id)   # not serializable, 세션에는 obejct가 아닌 primitive 데이터 형식만 저장 가능
        request.session["favorite_review"] = review_id

        # 리다이렉션용
        fav_review_user_name = Review.objects.filter(pk=review_id)[0].user_name
        return HttpResponseRedirect("/review-detail/" + fav_review_user_name)

    


