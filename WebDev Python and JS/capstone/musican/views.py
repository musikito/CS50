import json
from sre_parse import CATEGORIES
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Comments, Playlist, SongInfo


REGISTER = "musican/register.html"
LOGIN = "musican/login.html"
PLAYLIST = "musican/playlist.html"
HOME = "musican/index.html"


def index(request):
    return render(request, "musican/index.html", {
        "music": SongInfo.objects.all()
    })


def load_allsongs(request):

    songs = SongInfo.objects.all()
    songs = songs.order_by("-posted_on").all()

    return JsonResponse([song.serialize() for song in songs], safe=False)


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


def user_profile(request, username):
    user = User.objects.get(username=username)
    # user_posts = Posts.objects.filter(poster=user)
    # pages = Paginator(user_posts, 10)
    # This ATTRIBS come from the models related_name
    following = user.user_following.all()
    followers = user.user_followers.all()

    check_follow = False
    for i in followers:
        if request.user.username == i.follower.username:
            check_follow = True

    context = {
        "username": username,
        # "posts": user_posts,
        "following": following,
        "followers": followers,
        "check_follow": check_follow,
        # "pages": pages,
    }

    return render(request, "network/profile.html", context)


def add_to_playlist(request, listing_id):
    playlist = SongInfo.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    if not user.watchlist.filter(item_watched=playlist):

        watchlist = Playlist()
        watchlist.user = user
        watchlist.item_watched = playlist
        watchlist.save()
        return render(request, PLAYLIST, {
            "listing": playlist,
            # "form": BidForm(),
            "message": "Item was added to your wishlist",
            "msg_type": "success"

        })
    else:
        user.watchlist.filter(item_watched=playlist).delete()
        return render(request, PLAYLIST, {
            "listing": playlist,
            # "form": BidForm(),
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
