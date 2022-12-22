from sre_parse import CATEGORIES
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Comments, Playlist, SongInfo, Artist, Genre
from .forms import *

REGISTER = "musican/register.html"
LOGIN = "musican/login.html"
PLAYLIST = "musican/playlist.html"
HOME = "musican/index.html"
PLAYER = "musican/show_player.html"


def index(request):
    return render(request, HOME, {
        "songs": SongInfo.objects.all()
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
def create_genre(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = GenreForm(request.POST, request.FILES)

        if form.is_valid():
            genre = form.save(commit=False)
            genre.owner = user
            genre.save()
            return render(request, "musican/genre.html", {
                "message": "Genre was added",
                "msg_type": "success"
            })
    else:
        return render(request, "musican/create_genre.html", {
            "form": GenreForm()
        })


def genre_list(request):
    return render(request, "musican/genre_list.html", {
        "genres": Genre.objects.all()
    })


def genre(request, genre_name):
    genre_id = Genre.objects.get(pk=genre_name)

    return render(request, "musican/genre.html", {
        "genre": SongInfo.objects.filter(genre=genre_name),
        "genre_img": genre_id.genre_image,
        "genre_name": genre_id.genre_name
    })


@login_required(login_url='/login')
def create_artist(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = ArtistForm(request.POST, request.FILES)

        if form.is_valid():
            artist = form.save(commit=False)
            artist.owner = user
            artist.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "musican/create_artist.html", {
                "form": form
            })
    else:
        return render(request, "musican/create_artist.html", {
            "form": ArtistForm()
        })


def artists_list(request):
    return render(request, "musican/artists_list.html", {
        "artists": Artist.objects.all()
    })


def artist(request, artist_name):
    artist_id = Artist.objects.get(pk=artist_name)

    return render(request, "musican/artist.html", {
        "artist": SongInfo.objects.filter(artist=artist_name),
        "artist_img": artist_id.picture,
        "artist_name": artist_id.artist_name,
        "artist_bio": artist_id.bio
    })


@login_required(login_url='/login')
def create_song(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = SongsListingForm(request.POST, request.FILES)

        if form.is_valid():
            song = form.save(commit=False)
            song.owner = user
            song.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "musican/create_song.html", {
                "form": form
            })
    else:
        return render(request, "musican/create_song.html", {
            "form": SongsListingForm()
        })


@login_required(login_url='/login')
def add_to_playlist(request, song_id):
    song = SongInfo.objects.get(pk=song_id)
    user = User.objects.get(username=request.user)
    if not user.playlist.filter(song_added=song):
        playlist = Playlist()
        playlist.user = user
        playlist.song_added = song
        playlist.save()
        return render(request, PLAYER, {
            "song": song,
            "added": True,
            "message": "Song was added to your playlist",
            "msg_type": "success"
        })
    else:
        user.playlist.filter(song_added=song).delete()
        return render(request, PLAYER, {
            "song": song,
            "removed": True,
            "message": "The song was removed from your playlist",
            "msg_type": "danger"
        })


@ login_required(login_url='/login')
def playlist(request):
    user = User.objects.get(username=request.user)
    # https://docs.djangoproject.com/en/dev/ref/models/querysets/
    # https://stackoverflow.com/questions/21566017/parsing-the-django-model-results
    # mylist = watchlist.objects.get(user=request.user)
    return render(request, "musican/playlist.html", {
        "mylist": user.playlist.all()
    })


def show_player(request, song_id):
    return render(request, PLAYER, {
        "song": SongInfo.objects.get(pk=song_id)
    })


@ login_required(login_url='/login')
def comments(request, listing_id):
    listing = SongInfo.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    comment = Comments()
    comment.comment = request.POST.get("comment")
    comment.user = user
    comment.save()
    listing.comments.add(comment)
    listing.save()

    return render(request, "auctions/list_item.html", {
        "listing": listing,
        "message": "Your comment was added.",
        "msg_type": "success"
    })
