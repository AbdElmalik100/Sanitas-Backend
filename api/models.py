from django.db import models
from accounts.models import CustomUser

# Create your models here.


class ProductStore(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to='uploads', blank=True, null=True)
    code = models.CharField(max_length=255)

class ProductComponent(models.Model):
    name = models.CharField(max_length=255)

class DiseaseType(models.Model):
    name = models.CharField(max_length=255)

class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_orders')
    product = models.ForeignKey(ProductStore, on_delete=models.CASCADE, related_name='product_orders')


class MeatDetection(models.Model):
    image = models.ImageField(upload_to='meat_detection', blank=True, null=True)
    result = models.CharField(max_length=255, blank=True, null=True)
    result_class = models.CharField(max_length=255 ,blank=True, null=True)