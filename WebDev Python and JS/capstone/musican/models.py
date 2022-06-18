from multiprocessing import AuthenticationError
from xml.dom.pulldom import default_bufsize
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ImageField


class User(AbstractUser):
    pass


# Really a bad way to do the Categories
# this needs to be either a DB table
# or some new way
GENRE = (
    ('a', 'Electronics'),
    ('b', 'Collectibles & Art'),
    ('c', 'Home & Garden'),
    ('d', 'Clothing, Shoes & Accessories'),
    ('e', 'Toys & Hobbies'),
    ('f', 'Sporting Goods'),
    ('g', 'Books, Movies & Music'),
    ('h', 'Misc.')

)

# A model needs to be declared before been used by another model
# In order to use Bids i the Auction_listings model below.


class Bids(models.Model):
    current_bid = models.IntegerField(default=0)


# https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/

class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commenter')
    comment_date = models.DateTimeField(auto_now_add=True)


class Auction_Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    # Changed to use ImageField, install Pillow via pip3
    # https://docs.djangoproject.com/en/4.0/topics/files/
    # https://docs.djangoproject.com/en/4.0/topics/files/
    image = models.ImageField(null=True, blank=True)
    # image = models.CharField(max_length=200, blank=True, null=True)
    # Could this be an array?
    # Or a table from a DB
    category = models.CharField(
        max_length=1, choices=GENRE, default=GENRE[7][1])
    active = models.BooleanField(blank=True, default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner')
    starting_bid = models.IntegerField(default=0)
    current_bid = models.IntegerField(default=0)
    bids = models.ManyToManyField(
        Bids, blank=True, related_name="bids")
    time_added = models.DateTimeField(auto_now_add=True, blank=True)
    # Need to add time_to_end

    comments = models.ManyToManyField(
        Comments, blank=True, related_name="comments")


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watchlist')
    item_watched = models.ForeignKey(
        Auction_Listings, on_delete=models.CASCADE, related_name='item_watched')


class CategoryList(models.Model):
    cat_name = models.ForeignKey(
        Auction_Listings, on_delete=models.CASCADE, related_name='cat_name')
