import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    # 클래스 변수 = 데이터베이스 필드(컬럼)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("published_at")
    up_date = models.DateTimeField("edited_at")
    fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text
    
    # 버그가 있는 기능
    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # 버그 개선
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text