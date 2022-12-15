from multiprocessing import AuthenticationError
from xml.dom.pulldom import default_bufsize
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ImageField

from capstone.settings import MP3_URL


class User(AbstractUser):
    pass


# https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/

class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commenter')
    comment_date = models.DateTimeField(auto_now_add=True)


class Genre(models.Model):
    genre_name = models.CharField(max_length=14, null=True, blank=True)
    genre_image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.genre_name


class Artist(models.Model):
    artist_name = models.CharField(max_length=14)
    picture = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    featured_artist = models.BooleanField(default=False)
    liked_by = models.ForeignKey(
        User, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='artist_liked_by')
    num_likes = models.IntegerField(default='0')
    is_liked = models.BooleanField(
        default=None, null=True)

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return self.artist_name


class SongInfo(models.Model):
    title = models.CharField(max_length=30)
    song = models.FileField(upload_to=MP3_URL)
    picture = models.ImageField(null=True, blank=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='song_artist')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, null=True, blank=True, related_name="genre")
    duration = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    played_on = models.DateTimeField(auto_now_add=True)
    featured_song = models.BooleanField(default=False)
    liked_by = models.ForeignKey(
        User, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='liked_by')
    num_likes = models.IntegerField(default='0')
    is_liked = models.BooleanField(
        default=None, null=True)

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            "title": self.title,
            "song_url": self.song,
            "picture": self.picture,
            "artist_name": self.artist,
            "duration": self.duration,
            "genre": self.genre,
        }


class Playlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='playlist')
    song_added = models.ForeignKey(
        SongInfo, on_delete=models.CASCADE, related_name='song_added')
