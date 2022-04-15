import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import network

from .models import User, Posts


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


def load_allposts(request):
    logged_in = request.user.is_authenticated
    if logged_in:
        posts = Posts.objects.filter(user=request.user)
        print("logged in")
    else:
        posts = Posts.objects.all()
        print("not logged in")

    # Return posts latest to oldest
    posts = posts.order_by("-posted_on").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)

    # return HttpResponse(status=204)


@csrf_exempt
@login_required(login_url='/login')
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
