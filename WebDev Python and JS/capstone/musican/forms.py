from django.forms import ModelForm

# https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/

# Import everything from models
from .models import *


class AuctionListForm(ModelForm):
    class Meta:
        model = Auction_Listings
        fields = ["title", "description", "image",
                  "category", "active", "starting_bid"]


class BidForm(ModelForm):
    class Meta:
        model = Genre
        fields = ["genre_name", "genre_image"]


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
