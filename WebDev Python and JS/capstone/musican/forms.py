from django.forms import ModelForm

# https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/

# Import everything from models
from .models import SongInfo, Genre, Artist, Comments


class SongsListingForm(ModelForm):
    class Meta:
        model = SongInfo
        fields = ["title", "song", "picture", "artist",
                  "genre", "description", "featured_song"]

    def __init__(self, *args, **kwargs):
        super(SongsListingForm, self).__init__(*args, **kwargs)
        self.fields['artist'].queryset = Artist.objects.all()


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ["genre_name", "genre_image", "description"]


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ["artist_name", "picture", "bio", "featured_artist"]


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
