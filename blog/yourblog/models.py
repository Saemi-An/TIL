from datetime import date

from django.db import models
from django.core.validators import EmailValidator
from django.urls import reverse

# Create your models here.

    #    "slug": "hike-in-the-mountains",
    #     "image": "mountains.jpg",
    #     "author": "Maximilian",
    #     "date": date(2021, 7, 21),
    #     "title": "Mountain Hiking",
    #     "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
    #     "content": "Lorem"

class Tag(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.tag}"

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, blank=True)   # 이메일 없을 수 있음

    def __str__(self):
        return f"{self.last_name} / {self.email}"

class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=400)
    image_name = models.CharField(max_length=30, blank=True)   # 포스팅시 이미지 등록은 선택 --> 기본 이미지 파일 및 세팅 추가하기
    date = models.DateTimeField(auto_now=False, auto_now_add=True,)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False,)   # auto_now(저장 할때마다 현재시간 찍기)=False, auto_now_add(최초 작성시 현재시간 찍기)=True
    slug = models.SlugField(db_index=True)
    content = models.TextField()
    hide_post = models.BooleanField(default=False)   # EXTRA
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")
    tag = models.ManyToManyField(Tag, blank=True)   # 태그 없을 수 있음

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])
    
    def __str__(self):
        return f"{self.title} / {self.author.last_name}"
    
    
