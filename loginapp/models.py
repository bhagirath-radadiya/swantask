from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class User(models.Model):
    firstname = models.CharField(max_length=20, null=False, blank=False)
    lastname = models.CharField(max_length=20, null=False, blank=False)
    username = models.CharField(max_length=250, null=False, blank=False)
    password = models.CharField(max_length=10, null=False, blank=False)

    # def __str__(self):
    #     return self.username


class ShippingAddress(models.Model):
    address_line_1 = models.CharField(max_length=30, null=False, blank=False)
    address_line_2 = models.CharField(max_length=30)
    city = models.CharField(max_length=10, null=False, blank=False)
    state = models.CharField(max_length=10, null=False, blank=False)
    zipcode = models.IntegerField(null=False, blank=False)
    country = models.CharField(max_length=10, null=False, blank=False)


class Profile(models.Model):
    mobile_number = PhoneNumberField(null=False, blank=False, unique=True)
    alternate_mobile_number = PhoneNumberField(unique=True)
    addresses = models.ManyToManyField(ShippingAddress)
    user_id = models.ForeignKey(User, models.CASCADE)

    # def __str__(self):
    #     return str(self.user_id_id) + "-" + self.user_id.username
