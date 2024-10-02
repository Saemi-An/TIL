from django.db import models

# Create your models here.

class UserProfile(models.Model):
    image = models.ImageField(upload_to="images")   # 이미지 파일은 하드 드라이브에 저장한다, DB에는 해당 하드드라이브 경로를 저장한다