# Form Classes - 폼타입 / 인풋타입 / 폼 확인 규칙

from django import forms

from .models import Review

# class ReviewForm(forms.Form):
#     user_name = forms.CharField(label="이름", max_length=10, error_messages={
#         "required" : "이름을 입력해 주세요.",
#         "max_length" : "최대 10자까지 입력이 가능합니다.",
#     })
#     user_email = forms.EmailField(label="이메일", max_length=35, error_messages={
#         "required" : "이메일을 입력해 주세요.",
#         "required" : "최대 30자까지 입력이 가능합니다.",
#     })
#     review_text = forms.CharField(label="평가", widget=forms.Textarea, max_length=200)
#     rating = forms.IntegerField(label="별점", min_value=1, max_value=5)


class ReviewForm(forms.ModelForm):   # ModelForm
    class Meta:
        model = Review   # 어떤 모델을 폼으로 만들건지 지정 => 추후에 폼을 통해 유저로부터 전송받은 데이터를 DB에 저장할 때, 어느 테이블에 저장하는지 지표가 됨
        # fields = "__all__"   # 모델의 (id를 제외한)모든 속성을 폼으로 만들겠다
        exclude = ["user_email"]   # [ ]안의 속성을 제외한 모든 속성을 폼으로 만들겠다
        # fields = ["user_name", "review_text", "rating"]   # [ ]안에 있는 것들만 폼으로 만들겠다 
        labels = {   # ModelForm에서 레이블 이름 설정
            "user_name" : "이름",
            "review_text" : "리뷰",
            "rating" : "별점",
        }
        error_messages = {
            "user_name" : {
                "required" : "필수 입력값 입니다.",
                "max_length" : "최대 10자까지 입력이 가능합니다.",
            },
            "review_text" : {
                "required" : "필수 입력값 입니다.",
                "max_length" : "최대 200자까지 입력이 가능합니다.",
            },
        }