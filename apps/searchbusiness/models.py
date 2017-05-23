from django.db import models

# Create your models here.


class Business(models.Model):
    business_id = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=500)
    logo = models.CharField(max_length=800)
    address = models.CharField(max_length=800)
    phone_number = models.CharField(max_length=800)
    url = models.CharField(max_length=800)
