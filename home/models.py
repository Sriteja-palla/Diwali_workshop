from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Crackers(models.Model):
    cracker_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    age_range = models.CharField(max_length=30)
    choices = [
        ('a', "Gaalloo"),
        ('n', "Bhummida")
    ]
    type_of_cracker = models.CharField(max_length=1, choices=choices)
    image = models.ImageField(upload_to="Assets")

    def __str__(self):
        return self.cracker_name

class Sweets(models.Model):
    sweet_name = models.CharField(max_length=100)
    s_price = models.PositiveBigIntegerField()
    w_choices = [
        ('kg', 'kilogram'),
        ('g', 'gram')
    ]
    s_quantity = models.CharField(max_length=32)
    weight = models.CharField(max_length=32 ,default='1kg')
    s_image = models.ImageField(upload_to="Assets")

    def __str__(self):
        return self.sweet_name

class Gifts(models.Model):
    gift_name = models.CharField(max_length=100)
    gift_price = models.PositiveBigIntegerField()
    gift_quantity = models.PositiveBigIntegerField()
    gift_image = models.ImageField(upload_to="Assets")

    def __str__(self):
        return self.gift_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cracker = models.ForeignKey(Crackers, on_delete=models.CASCADE, null=True, blank=True)
    sweet = models.ForeignKey(Sweets, on_delete=models.CASCADE, null=True, blank=True)
    gift = models.ForeignKey(Gifts, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - Cart"