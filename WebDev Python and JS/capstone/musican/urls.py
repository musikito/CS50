from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_artist", views.create_artist, name="create_artist"),
    path("artists_list", views.artists_list, name="artists_list"),
    path("artist/<int:artist_name>", views.artist, name="artist"),
    path("create_song", views.create_song, name="create_song"),
    path("playlist", views.playlist, name="playlist"),
    path("add_to_playlist/<int:song_id>",
         views.add_to_playlist, name="add_to_playlist"),
    path("show_player/<int:song_id>", views.show_player, name="show_player"),
    path("create_genre", views.create_genre, name="create_genre"),
    path("genre_list", views.genre_list, name="genre_list"),
    path("genre/<int:genre_name>", views.genre, name="genre"),

    path("comments/<int:listing_id>", views.comments, name="comments"),

]
