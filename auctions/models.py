from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.ImageField()
    category = models.CharField(max_length=64)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_price = models.IntegerField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)

class Category(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    fashion = BooleanField()
    toys = BooleanField()
    electronics = BooleanField()
    home = BooleanField()
