from django.urls import path
from musican import views

urlpatterns = [
    path('api/musican/', views.GenreListCreate.as_view()),
]
