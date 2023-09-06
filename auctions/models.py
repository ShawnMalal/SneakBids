from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model): 
    categoryName = models.CharField(max_length=64)
    

    def __str__(self):
        return self.categoryName


class Listings(models.Model): 
    itemName = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    imageUrl = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.itemName





