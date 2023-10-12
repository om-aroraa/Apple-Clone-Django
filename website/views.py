import random
from database.models import users, mobiles, ipads, cart, MacBooks
from django.shortcuts import render, redirect
from django.http import HttpResponse
from database.forms import deviceForm

# Create your views here.
def home(request):
    username = request.session.get('username')
    if username:
        c = cart.objects.get(name=username)
        cart_items = c.items
        if cart_items:
            cart_items = len(cart_items.split(','))
        else:
            cart_items = 0
        cart_total = cart_items 
        return render(request, "main.html", {'username': username, 'cart_total': cart_total})
    else:
        return render(request, "main.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('pswd')
        try:
            user = users.objects.get(name=username, password=password)
            request.session['username'] = username
            return redirect('/')
        except:
            return render(request, "login.html", { 'error': 'Invalid username or password' })
    else:
        username = request.session.get('username')
        if username:
            return redirect('/')
        else:
            return render(request, "login.html")

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('/login')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('pswd')
        try:
            user = users.objects.get(name=username)
            return render(request, "signup.html", { 'error': 'Username already exists' })
        except:
            user = users(name=username, password=password)
            c = cart(name=username, items="")
            user.save()
            c.save()
            request.session['username'] = username
            return redirect('/')
    else:
        username = request.session.get('username')
        if username:
            return redirect('/')
        else:
            return render(request, "signup.html")
        
def menu(request):
    username = request.session.get('username')
    type = request.GET.get('type')
    data = None
    if type == 'iphones':
        items = mobiles.objects.all()
        data = list(items)
    elif type == 'ipads':
        items = ipads.objects.all()
        data = list(items)
    elif type == 'macbooks':
        items = MacBooks.objects.all()
        data = list(items)
    else:
        type = 'iphones'
        items = mobiles.objects.all()
        data = list(items)
    if username:
        c = cart.objects.get(name=username)
        cart_items = c.items
        if cart_items:
            cart_items = len(cart_items.split(','))
        else:
            cart_items = 0
        cart_total = cart_items 
        return render(request, "menu.html", {'username': username, 'cart_total': cart_total, 'data': data, 'type': type})
    else:
        return render(request, "menu.html", {'data': data, 'type': type})

def checkout(request):
    return render(request, "checkout.html")