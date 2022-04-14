from django.shortcuts import render, redirect
from . import models
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData
from django.contrib.auth.forms import UserCreationForm
from .forms import newUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.db.models import Q
from django.core.mail import send_mail

# Create your views here.

class SearchResultsView(ListView):
    model = models.Product
    template_name = 'store/search.html'
    context_object_name = 'products'


    def get(self, request, *args, **kwargs):
        
        data = cartData(request)
        cartItems = data['cartItems']
        query = self.request.GET.get('search')
        products = models.Product.objects.filter(Q(name__icontains=query))
        context = {'products': products,'cartItems': cartItems}
        return render(request, 'store/search.html', context=context)


def register_user(request):
    form = newUserForm()
    if request.method == 'POST':
        form = newUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = models.Customer.objects.create(
                user=user,
                email=form.cleaned_data['email'],
                name=form.cleaned_data['username']
            )
            customer.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'store/register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Please enter valid details')

    context = {}
    return render(request, 'store/login.html', context)

def logout_user(request):
    logout(request)
    return redirect("store")

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = models.Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    

    customer = request.user.customer
    product = models.Product.objects.get(id=productId)
    order, created = models.Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def orderProcess(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print('User is not logged in')
        print('COOKIES:', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = models.Customer.objects.get_or_create(
            email=email,
        )
        customer.name = name
        customer.save()

        order = models.Order.objects.create(
            customer=customer,
            complete=False
        )

        for item in items:
            product = models.Product.objects.get(id=item['product']['id'])
            orderItem = models.OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.cart_total):
        order.complete = True
    order.save()

    if order.shipping is True:
        models.ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            contact=data['shipping']['contact'],
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('Payment Complete', safe=False)
