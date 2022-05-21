
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.createpost, name="create_post"),
    path("load_allposts", views.load_allposts, name="load_allposts"),
    path("user_profile/<str:username>", views.user_profile, name="user_profile"),
    path("follow_user/<str:username>", views.follow_user, name="follow_user"),
    path("unfollow_user/<str:username>",
         views.unfollow_user, name="unfollow_user"),
    path("likes", views.likes, name='likes')
]
