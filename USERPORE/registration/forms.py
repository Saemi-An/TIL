from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class RegisterForm(forms.Form):
    PD_TYPE_CHOICES = [
        (1, "휘낭시에"),
        (2, "조각케이크"),
        (3, "스콘"),
        (4, "특별메뉴"),
    ]

    pd_type = forms.ChoiceField(choices=PD_TYPE_CHOICES, widget=forms.Select, label="상품 종류", error_messages={
        "required" : "상품 종류를 선택해 주세요.",
    })
    pd_name = forms.CharField(max_length=20, label="상품명", error_messages={
        "required" : "상품 이름을 입력해 주세요.",
        "max_length" : "최대 20자의 상품명을 입력해 주세요.",
    })
    pd_note = forms.CharField(max_length=200, required=False, label="상품 설명", widget=forms.Textarea, error_messages={
        "max_length" : "최대 300자의 상품 설명을 입력해 주세요.",

    })
    pd_price = forms.IntegerField(label="상품 가격", error_messages={
        "required" : "상품 가격을 입력해 주세요.",
    })
    pd_img = forms.ImageField(label="상품 이미지", error_messages={
            "required" : "상품 이미지를 등록해 주세요.",
    })


    