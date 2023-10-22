from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
import datetime

# Create your models here.

# model for storing captcha data
class captchaCpde(models.Model):
    sno=models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="img/captchaImgs", default='')
    value=models.CharField(max_length=5,default="")

    def __str__(self):
        return self.value 

# model for storing products data
class allProducts(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="img/allProducts/%Y/%m", default='')
    title = models.CharField(max_length=200, default="")
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default='Other')
    desc = models.TextField(max_length=5000, default='')
    time = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.category

#  model for adding product in cart
class productsCart(models.Model):
    sno = models.AutoField(primary_key=True)
    usrname = models.ForeignKey(User,on_delete=models.CASCADE)
    prod_ids = models.JSONField(default=dict)

# model for storing comments
class productComment(models.Model):
    sno = models.AutoField(primary_key=True)
    usr = models.ForeignKey(User,on_delete=models.CASCADE)
    usrname = models.CharField(max_length=50, default='anonymous')
    product_id = models.IntegerField(default=0)
    comment = models.TextField(max_length=200, default="")
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment