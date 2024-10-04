from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Product(models.Model):
    pd_type = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    pd_name = models.CharField(max_length=20)
    pd_note = models.CharField(max_length=200, blank=True)
    pd_price = models.IntegerField()
    pd_img = models.ImageField(upload_to="pd_images")

    def __str__(self):
        return f"{self.pd_name}, {self.pk}"