import random
from database.models import users, mobiles, ipads, cart, MacBooks
from django.shortcuts import render, redirect
from django.http import HttpResponse
from database.forms import deviceForm
# csrf_exempt
from django.views.decorators.csrf import csrf_exempt

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
        return redirect('/')
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
    username = request.session.get('username')
    if request.method == "POST":
        c = cart.objects.get(name=username)
        c.items = ""
        c.save()
        return HttpResponse(
            '<h1>Thank you for shopping with us!</h1><br><a href="/">Go back to home page</a>'
        )
    if username:
        c = cart.objects.get(name=username)
        cart_items = c.items
        cc = []
        if cart_items:
            cart_items = cart_items.split(',')
            cart_total = len(cart_items)
            for i in cart_items:
                try:
                    id = i.split('-')[0]
                    type = i.split('-')[1]
                    if type == 'iphones':
                        item = mobiles.objects.get(id=id)
                    elif type == 'ipads':
                        item = ipads.objects.get(id=id)
                    elif type == 'macbooks':
                        item = MacBooks.objects.get(id=id)
                    cc.append(item)
                except:
                    pass
        else:
            cart_items = 0
            cc = None
            cart_total = cart_items
        print(cc)
        return render(request, "checkout.html", {'username': username, 'cart_total': cart_total, 'cart_items': cc})
    else:
        return redirect('/login')

@csrf_exempt
def product(request):
    if request.method == "POST":
        id = request.POST.get('id')
        type = request.POST.get('type')
        if type == 'iphones':
            item = mobiles.objects.get(id=id)
        elif type == 'ipads':
            item = ipads.objects.get(id=id)
        elif type == 'macbooks':
            item = MacBooks.objects.get(id=id)
        else:
            return redirect('/')
        c = cart.objects.get(name=request.session.get('username'))
        items = c.items
        if items:
            items = items + str(id)+"-"+type + ','
        else:
            items = str(id)+"-"+type + ','
        c.items = items
        c.save()
        return redirect('/checkout')
    else:
        id = request.GET.get('id')
        type = request.GET.get('type')
        if type == 'iphones':
            item = mobiles.objects.get(id=id)
        elif type == 'ipads':
            item = ipads.objects.get(id=id)
        elif type == 'macbooks':
            item = MacBooks.objects.get(id=id)
        else:
            return redirect('/')
        username = request.session.get('username')
        if username:
            c = cart.objects.get(name=username)
            cart_items = c.items
            if cart_items:
                cart_items = len(cart_items.split(','))
            else:
                cart_items = 0
            cart_total = cart_items 
            return render(request, "product.html", {'username': username, 'cart_total': cart_total, 'item': item, 'type': type})
        else:
            return render(request, "product.html", {'item': item, 'type': type})

def manage(request):
    username = request.session.get('username')
    if username != 'admin':
        return redirect('/')
    else:
        if request.method == "GET":
            type = request.GET.get('type')
            if type == "Add":
                form = deviceForm()
            else:
                form = None
            return render(request, "manage.html", {'action': type, 'username': username, 'form': form})
        else:
            type = request.POST.get('type')
            action = request.POST.get('action')
            if action == "Add":
                form = deviceForm(request.POST, request.FILES)
                if form.is_valid():
                    if type == 'iphones':
                            item = mobiles(name=form.cleaned_data['name'], price=form.cleaned_data['price'], image=form.cleaned_data['image'], description=form.cleaned_data['description'])
                            item.save()
                            return render(request, "manage.html", {'type': type, 'username': username, 'form': form, 'error': 'Item added successfully'})
                    elif type == 'ipads':
                            item = ipads(name=form.cleaned_data['name'], price=form.cleaned_data['price'], image=form.cleaned_data['image'], description=form.cleaned_data['description'])
                            item.save()
                            return render(request, "manage.html", {'type': type, 'username': username, 'form': form, 'error': 'Item added successfully'})
                    elif type == 'macbooks':
                            item = MacBooks(name=form.cleaned_data['name'], price=form.cleaned_data['price'], image=form.cleaned_data['image'], description=form.cleaned_data['description'])
                            item.save()
                            return render(request, "manage.html", {'type': type, 'username': username, 'form': form, 'error': 'Item added successfully'})
                    else:
                        return render(request, "manage.html", {'type': type, 'username': username, 'form': form, 'error': 'Invalid type'})
                else:
                    print(form.errors)
                    return redirect('/manage?type=' + action)
            else:
                id = request.POST.get('id')
                try:
                    if type == 'iphones':
                        item = mobiles.objects.get(id=id)
                        item.delete()
                        return render(request, "manage.html", {'type': type, 'username': username, 'error': 'Item deleted successfully'})
                    elif type == 'ipads':
                        item = ipads.objects.get(id=id)
                        item.delete()
                        return render(request, "manage.html", {'type': type, 'username': username, 'error': 'Item deleted successfully'})
                    elif type == 'macbooks':
                        item = MacBooks.objects.get(id=id)
                        item.delete()
                        return render(request, "manage.html", {'type': type, 'username': username, 'error': 'Item deleted successfully'})
                    else:
                        return render(request, "manage.html", {'type': type, 'username': username, 'error': 'Invalid type'})
                except:
                    return render(request, "manage.html", {'type': type, 'username': username, 'error': 'Item not found'})