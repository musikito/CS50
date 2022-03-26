from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry"),
    path("random_entry", views.random_entry, name="random_entry")

]
