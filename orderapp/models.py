from django.db import models
from django.contrib.postgres.fields import JSONField
from loginapp.models import User

# Create your models here.


class Order(models.Model):
    product = JSONField()
    totalPrice = models.FloatField()
    orderDate = models.DateField(null=True)
    orderstatus = models.CharField(max_length=10, default='addtocart')
    paymentstatus = models.CharField(max_length=50, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10,null=True)
    discount = models.FloatField(null=True)
    tax = models.FloatField(null=True)
    grandTotal= models.FloatField()
    userDetail = models.CharField(max_length=150,null=True)
