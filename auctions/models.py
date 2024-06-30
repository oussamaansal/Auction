from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=50)
    image =   models.URLField(blank=True) 
    def __str__(self):
        return self.title


class Auction(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    start_bid = models.IntegerField(default=0)
    desc = models.CharField(max_length=200)
    categ = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)  # Field to indicate if the auction is active
    winner = models.ForeignKey(User, null=True, blank=True, related_name='won_auctions', on_delete=models.SET_NULL)  # Field to store the winner

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
     return f"{self.user.username} - {self.auction.title} - {self.amount}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
     return f"{self.user.username} - {self.auction.title} - {self.text}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.auction.title}"