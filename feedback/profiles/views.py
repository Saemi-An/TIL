from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .forms import ProfileForm
from .models import UserProfile

class ProfilesView(ListView):
    template_name = "profiles/user_profiles.html"
    model = UserProfile
    context_object_name = "profiles"


# 3단계: Profile 뷰
class CreateProfileView(CreateView):
    template_name = "profiles/create_profile.html"
    model = UserProfile
    fields = "__all__"
    success_url = "/profiles"

# 1단계: 파일 업로드 표준
# def store_file(file):
#     with open("temp/image.jpg", "wb+") as dest:   # wb+ : binaryfile 을 지정 위치에 write 한다
#         for chunk in file.chunks():
#             dest.write(chunk)

# 2단계: ProfileForm 폼 + UserProfile 모델
# class CreateProfileView(View):
#     def get(self, request):
#         form = ProfileForm()
#         return render(request, "profiles/create_profile.html", {
#             "form" : form,
#         })

#     def post(self, request):
#         # request.POST   # none-file data에 접근 가능
#         # store_file(request.FILES["image"])   # 1단계
#         submitted_form = ProfileForm(request.POST, request.FILES)

#         if submitted_form.is_valid():
#             profile = UserProfile(image=request.FILES["user_image"])
#             profile.save()
#             return HttpResponseRedirect("/profiles")

#         return render(request, "profiles/create_profile.html", {
#             "form" : submitted_form,
#         })