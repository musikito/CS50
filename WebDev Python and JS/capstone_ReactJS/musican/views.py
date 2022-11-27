from django.shortcuts import render

# Create your views here.
from musican.models import Genre
from musican.serializer import GenreSerializer
from rest_framework import generics


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all().order_by('-genre_name')
    serializer_class = GenreSerializer
