from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify   # str을 slug로 변환시킴

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Countries"   # 어드민에서 나타나는 이름 바꾸기


class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"
    
    # nested class, Meta Configuration ???
    class Meta:
        verbose_name_plural = "Address Entries"

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


# 책 한권이 갖는 데이터 구조를 정의
class Book(models.Model):   # Model 클래스 상속
    title = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # author = models.CharField(null=True, max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(default="", null=False, db_index=True)   # slug format: Harry Potter 1 => harry-potter-1
    published_country = models.ManyToManyField(Country, null=False)   # related_name="books"

    def get_absolute_url(self):
        return reverse("book_detail", args=[self.slug])
    
    # overwriting built-in save() method
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)   # 빌트인 save() 함수 호출

    def __str__(self):   # 파이썬 빌트인 함수, 인스턴스가 터미널에 어떻게 출력되어야 할지 명령한다
        return f"{self.title} ({self.pk})"
        