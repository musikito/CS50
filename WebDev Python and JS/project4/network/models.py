import re
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tweets")
    poster = models.ForeignKey(
        User, default=None, on_delete=models.PROTECT, related_name="author")
    content = models.CharField(max_length=500, null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    liked_by = models.ForeignKey(
        User, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='liked_by')
    num_likes = models.IntegerField(default='0')

    def serialize(self):
        return {

            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "posted_on": self.posted_on.strftime("%b %-d %Y, %-I:%M %p"),
            "liked_by":  self.liked_by,
            "num_likes": self.num_likes
        }
