from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    pass


# Auction Listing Model
class Listing(models.Model):
    title = models.CharField(validators=[MinLengthValidator(5)], max_length=50, default="")
    user_posted = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='auction_photo')
    startingPrice = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    uploadDate = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default= True)
    category = models.CharField(validators=[MinLengthValidator(1)], max_length=64)
    currentPrice = models.IntegerField(default=0)
    expire = models.DateTimeField(default=timezone.now() + timedelta(hours=24))

    def check_expired(self):
        if timezone.now() >= self.expire:
            self.active = False
            self.save()
    
    def __str__(self):
        return f"Listing by {self.user_posted} on {self.uploadDate}"


# Bids for listings
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
# Comments for Listing
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(validators=[MinLengthValidator(5)], max_length=100)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)