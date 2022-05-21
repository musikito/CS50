from enum import unique
import re
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """it makes sense to have the follow/unfollow stuff with the user"""

    def follow(self, usuario):
        FollowUser.objects.create(follower=self, following=usuario)

    def unfollow(self, usuario):
        FollowUser.objects.get(follower=self, following=usuario).delete()


class FollowUser(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_following")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_followers")

    # https://www.geeksforgeeks.org/meta-class-in-models-django/
    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f'{self.follower} follows {self.following}'


class Posts(models.Model):
    user = models.ForeignKey(
        User, default=None, on_delete=models.CASCADE, related_name="user_id")
    poster = models.ForeignKey(
        User, default=None, on_delete=models.PROTECT, null=True, blank=True, related_name="author")
    content = models.CharField(max_length=500, null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    liked_by = models.ForeignKey(
        User, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='liked_by')
    num_likes = models.IntegerField(default='0')
    is_liked = models.BooleanField(
        default=None, null=True)

    class Meta:
        ordering = ["-posted_on"]

    def serialize(self):
        return {
            "userid": self.user.id,
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "posted_on": self.posted_on.strftime("%b %-d %Y, %-I:%M %p"),
            # "liked_by":  self.liked_by.id,
            "num_likes": self.num_likes,
            "is_liked": self.is_liked
        }


'''using for the likes, maybe move it to the post model itself?'''
'''TODO move it to the post model'''


class Like(models.Model):
    liked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked")
    post_liked = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("liked_by", "post_liked")

    def __str__(self):
        return f"{self.liked_by} likes{self.post_liked}."


"""scratched this in favor of using the User model"""
# class Profile(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    follower = models.ManyToManyField(
#        User, blank=True, related_name="follower_user")
#    following = models.ManyToManyField(
#        User, blank=True, related_name="following_user")
