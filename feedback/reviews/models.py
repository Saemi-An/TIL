from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Review(models.Model):
    user_name = models.CharField(max_length=10)
    user_email = models.EmailField(max_length=35)
    review_text = models.TextField(max_length=200)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])