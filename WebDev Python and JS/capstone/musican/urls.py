from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("list_item/<int:listing_id>", views.list_item, name="list_item"),
    path("close_item/<int:listing_id>", views.close_item, name="close_item"),
    path("add_to_watchlist/<int:listing_id>",
         views.add_to_watchlist, name="add_to_watchlist"),
    path("comments/<int:listing_id>", views.comments, name="comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category_list", views.category_list, name="category_list"),
    path("category/<str:cat>", views.category, name="category")
]
