from sre_parse import CATEGORIES
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction_Listings, Bids, Comments, Watchlist
from .forms import *

REGISTER = "musican/register.html"
LOGIN = "musican/login.html"
PLAYLIST = "musican/playlist.html"


def index(request):
    return render(request, "musican/index.html", {
        "listings": Auction_Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, LOGIN, {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, LOGIN)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, REGISTER, {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, REGISTER, {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, REGISTER)


# See Documentation for this decorator:
# https://docs.djangoproject.com/es/4.0/topics/auth/default/
# Also: https://stackoverflow.com/questions/3578882/how-to-specify-the-login-required-redirect-url-in-django
@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = AuctionListForm(request.POST, request.FILES)
        # print("forma", form)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "musican/create_listing.html", {
                "form": form
            })

    else:
        return render(request, "musican/create_listing.html", {
            "form": AuctionListForm()
        })


@login_required(login_url='/login')
def close_item(request, listing_id):
    item = Auction_Listings.objects.get(pk=listing_id)
    item.active = False
    item.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login')
def add_to_watchlist(request, listing_id):
    listing = Auction_Listings.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    if not user.watchlist.filter(item_watched=listing):

        watchlist = Watchlist()
        watchlist.user = user
        watchlist.item_watched = listing
        watchlist.save()
        return render(request, PLAYLIST, {
            "listing": listing,
            "form": BidForm(),
            "message": "Item was added to your wishlist",
            "msg_type": "success"

        })
    else:
        user.watchlist.filter(item_watched=listing).delete()
        return render(request, PLAYLIST, {
            "listing": listing,
            "form": BidForm(),
            "message": "Your item was removed from the wishlist",
            "msg_type": "danger"

        })


@ login_required(login_url='/login')
def watchlist(request):
    user = User.objects.get(username=request.user)
    # https://docs.djangoproject.com/en/dev/ref/models/querysets/
    # https://stackoverflow.com/questions/21566017/parsing-the-django-model-results
    # mylist = watchlist.objects.get(user=request.user)
    return render(request, "musican/watchlist.html", {
        "mylist": user.watchlist.all()
    })


@ login_required(login_url='/login')
def list_item(request, listing_id):
    listing = Auction_Listings.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)

    # Owner/poster can't bid in his own listing
    if user == listing.owner:
        # print("usuario", listing.owner.username)
        return render(request, PLAYLIST, {
            "listing": listing,
            "message": "You own this listing",
            "msg_type": "danger",
            "list_owner": True

        })

    if request.method == "POST":

        # return HttpResponseRedirect(reverse('list_item', args=(listing.id,)))

        new_bid = int(request.POST["current_bid"])

        # Check if current bid is bigger then previous bid
        print("current bid", listing.current_bid)
        print("new bid", new_bid)
        if new_bid <= listing.current_bid:
            print("error")
            return render(request, PLAYLIST, {
                "listing": listing,
                "form": BidForm(),
                "message": "Your Bid needs to be greater than current price",
                "msg_type": "danger"

            })

        form = BidForm(request.POST)
        if form.is_valid():
            print("inside bid")
            bid = form.save(commit=False)
            bid.bidder = user
            bid.save()
            listing.bids.add(bid)
            listing.current_bid = new_bid
            listing.save()
            print("good bid")
            return render(request, PLAYLIST, {
                "listing": listing,
                "form": BidForm(),
                "message": "Your Bid is the current one",
                "msg_type": "success"

            })
        else:
            return render(request, PLAYLIST, {
                "form": form
            })
       # return HttpResponseRedirect(reverse('list_item', args=(listing.id,)))

    else:
        return render(request, PLAYLIST, {
            "listing": listing,
            "form": BidForm(),
            "message": "",

        })


@ login_required(login_url='/login')
def comments(request, listing_id):
    listing = Auction_Listings.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    comment = Comments()
    comment.comment = request.POST.get("comment")
    comment.user = user
    comment.save()
    listing.comments.add(comment)
    listing.save()

    return render(request, PLAYLIST, {
        "listing": listing,
        "message": "Your comment was added.",
        "msg_type": "success"
    })


def category_list(request):
    return render(request, "musican/category_list.html", {
        "cats": CATS
    })


def category(request, cat):
    listings = Auction_Listings.objects.filter(category__in=cat)
    cats = dict(CATS)

    return render(request, "musican/index.html", {
        "listings": listings,
        "category": cats[cat]
    })

# def category_list(request):
#    listing = Auction_listings.objects.all()
#    return render(request, "musican/category_list.html", {
#        "cats": listing
#    })


# def category(request, cat):
#    category = Auction_listings.objects.get(category=cat)
#    print(category)

#    return render(request, "auction/list_item.html")
