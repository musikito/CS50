import re
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    content = models.CharField(max_length=500, null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        User, default=None, blank=True, related_name='liked_by')
    num_likes = models.IntegerField(default='0')
