
from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "hola/index.html")


def jose(request):
    return HttpResponse("Hola Jose!")


def saludos(request, nombre):
    return render(request, "hola/saludos.html", {
        "name": nombre.capitalize()
    })
