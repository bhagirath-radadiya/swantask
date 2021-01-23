from django.db import models

# Create your models here.

# name
# price
# category
# availibility

CATEGORY = (
    ('sneakers', 'Sneakers'),
    ('loafers', 'Loafers'),
    ('derby', 'Derby'),
)

BRAND = (
    ('puma', 'Puma'),
    ('adidas', 'Adidas'),
    ('woodland', 'Woodland'),
    ('red tap', 'Red Tap'),
    ('bata', 'Bata'),
)


class Product(models.Model):
    image = models.ImageField(upload_to='product')
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=10, choices=BRAND)
    price = models.IntegerField()
    category = models.CharField(max_length=10, choices=CATEGORY)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
