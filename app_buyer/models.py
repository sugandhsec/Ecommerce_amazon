from django.db import models
from app_seller.models import Products
# Create your models here.
class User(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    pic = models.FileField(upload_to='buyer_images',default='anonymous.jpg')

    def __str__(self):
        return self.fullname

class Cart(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    productid = models.ForeignKey(Products,on_delete=models.CASCADE)
    orderid = models.IntegerField()

    def __str__(self):
        return str(self.orderid)