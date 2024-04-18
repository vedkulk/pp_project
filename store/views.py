from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib import messages
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import CreateUserForm
# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, "The username or password is incorrect")
    return render(request, 'store/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def Registration(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        print("--------is valid", form.is_valid())
        print(form.error_messages)
        print(form.data["username"])
        if form.is_valid():
            user = form.save()
            username = form.data["username"]
            cust = Customer.objects.create(
                user=user,
                name=username
            )
            cust.save()
            messages.success(request, "Successfully Registered")
            return redirect('login')
    context = {'form': form}
    return render(request, 'store/Registration.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('Cart :', cart)
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart-items']

        for i in cart:
            try:
                cartItems += cart[i]["quantity"]
                product = Product.objects.get(id=i)
                total = (product.price*cart[i]['quantity'])

                order["get_cart_total"] += total
                order["get_cart_items"] += cart[i]['quantity']

                item = {

                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imgURL': product.imgURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                pass

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def product(request, pk):
    products = Product.objects.get(id=pk)
    context = {'products': products}
    return render(request, 'store/product.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']
    print('Action: ', action)
    print('ProductId: ', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added.', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(customer=customer, order=order,
                                           address=data['shipping']['address'], city=data['shipping']['city'],
                                           state=data['shipping']['state'], zipcode=data['shipping']['zipcode'])
    else:
        print("User is not logged in...")
    return JsonResponse('Payment completed', safe=False)
