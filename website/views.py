from database.models import users, mobiles, ipads, cart, orders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from database.forms import deviceForm

# Create your views here.
def home(request):
    return render(request, "main.html")

def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")