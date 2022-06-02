import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


from .models import FollowUser, Like, User, Posts


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user_profile(request, username):
    user = User.objects.get(username=username)
    user_posts = Posts.objects.filter(poster=user)
    pages = Paginator(user_posts, 10)
    # This ATTRIBS come from the models related_name
    following = user.user_following.all()
    followers = user.user_followers.all()

    check_follow = False
    for i in followers:
        if request.user.username == i.follower.username:
            check_follow = True

    context = {
        "username": username,
        "posts": user_posts,
        "following": following,
        "followers": followers,
        "check_follow": check_follow,
        "pages": pages,
    }

    return render(request, "network/profile.html", context)


@ csrf_exempt
@ login_required(login_url='/login')
def likes(request):
    if request.method == "POST":
        post_id = json.loads(request.body)
        like_user = request.user

        user = User.objects.get(username=like_user)
        post = Posts.objects.get(pk=post_id)
        num_likes = post.likes.all().count()

        Posts.objects.filter(pk=post_id).update(
            num_likes=num_likes, liked_by=user)

        try:

            Like.objects.create(liked_by=user, post_liked=post)
        except IntegrityError:
            # Posts.objects.filter(pk=post_id).update(is_liked=False)
            Like.objects.filter(liked_by=user, post_liked=post).delete()

        return JsonResponse(num_likes, safe=False)


def following(request):
    '''https://stackoverflow.com/questions/50431810/the-queryset-value-for-an-exact-lookup-must-be-limited-to-one-result-using-slici'''
    if request.user.is_authenticated:
        user = request.user
        users = User.objects.filter(user_followers__follower=user)
        posts = Posts.objects.filter(poster__in=users)
        context = {
            "posts": posts,
        }

        return render(request, "network/following.html", context)

    # return redirect("index")


def follow_user(request, username):
    followuser = User.objects.get(username=username)
    request.user.follow(followuser)
    return redirect("index")


def unfollow_user(request, username):
    unfollowuser = User.objects.get(username=username)
    request.user.unfollow(unfollowuser)
    return redirect("index")


def load_allposts(request):
    # logged_in = request.user.is_authenticated
    # if logged_in:
    #    posts = Posts.objects.filter(user=request.user)
    #    print("logged in")
    # else:
    posts = Posts.objects.all()
    # print("not logged in")
    # Return posts latest to oldest
    posts = posts.order_by("-posted_on").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


@ csrf_exempt
@ login_required(login_url='/login')
def createpost(request):

    data = json.loads(request.body)
    print("body", data.get("post", ""))

    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    # Get post data
    post = data.get("post", "")
    user = request.user
    postdata = Posts(
        user=user,
        poster=request.user,
        content=post
    )
    postdata.save()

    return JsonResponse({"message": "Post was a success"}, status=201)
