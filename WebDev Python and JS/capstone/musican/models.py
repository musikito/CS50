from multiprocessing import AuthenticationError
from turtle import title
from xml.dom.pulldom import default_bufsize
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, ImageField

from capstone.settings import MP3_URL


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


class Genre(models.Model):
    genre_name = models.CharField(max_length=14, null=True, blank=True)
    genre_image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.genre_name


class Artist(models.Model):
    artist_name = models.CharField(max_length=14)
    picture = models.ImageField(null=True, blank=True)
    links = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    liked_by = models.ForeignKey(User, default=None, blank=True,
                                 null=True, on_delete=models.CASCADE, related_name='liked_by')
    num_likes = models.IntegerField(default='0')
    posted_on = models.DateTimeField(auto_now_add=True)
    featured_artist = models.BooleanField(default=False)

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return self.artist_name


class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commenter')
    comment_date = models.DateTimeField(auto_now_add=True)


class SongInfo(models.Model):
    title = models.CharField(max_length=30)
    song = models.FileField(upload_to=MP3_URL)
    picture = models.ImageField(null=True, blank=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='song_artist')
    duration = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='song_genre')
    description = models.TextField(null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    played_on = models.DateTimeField(auto_now_add=True)
    featured_song = models.BooleanField(default=False)

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return self.title

# https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/


class Playlist(models.Model):
    playlist_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='playlist_user')
    playlist_title = models.CharField(max_length=30)
    playlist_song = models.ManyToManyField(SongInfo)
    posted_on = models.DateTimeField(auto_now_add=True)
    played_on = models.DateTimeField(auto_now_add=True)
    featured_playlist = models.BooleanField(default=False)

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return self.playlist_title


class AlbumInfo(models.Model):
    album_name = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)
    songs = models.ManyToManyField(SongInfo)
    album_cover = models.ImageField(null=True, blank=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='album_artist')
    description = models.TextField(null=True, blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='album_genre')
    posted_on = models.DateTimeField(auto_now_add=True)
    played_on = models.DateTimeField(auto_now_add=True)
    featured_album = models.BooleanField(default=False)

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return self.album_name


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
    # bids = models.ManyToManyField(
    #    Bids, blank=True, related_name="bids")
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
