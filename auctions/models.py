from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title} - {self.description} - {self.starting_bid} - {self.image} - {self.category} - {self.active} - {self.user}"
    
class Comment(models.Model):
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.comment} - {self.user} - {self.listing}"
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid} - {self.user} - {self.listing}"
    

