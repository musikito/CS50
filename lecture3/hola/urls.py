from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:nombre>", views.saludos, name="saludos"),
    path("jose", views.jose, name="jose")
]
