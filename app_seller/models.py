from django.db import models

# Create your models here.
class User_seller(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    pic = models.FileField(upload_to='seller_images',default='anonymous.jpg')

    def __str__(self):
        return self.fullname


class Products(models.Model):
    pname = models.CharField(max_length=30)
    price = models.FloatField()
    pic = models.FileField(upload_to='products',default='product.jpg')
    seller = models.ForeignKey(User_seller,on_delete=models.CASCADE)

    def __str__(self):
        return self.pname

        