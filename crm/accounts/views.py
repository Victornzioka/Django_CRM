from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Product, Customer, Order
from .forms import OrderForm, CustomerForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save()

            messages.success(request, f'Account created for {username}.')
            return redirect('/login')

    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user             #this is a decorator to make sure a logged in user wont see the login page
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is incorrect")
    return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')       #this is a decorator to make sure a user that is not logged in won't access this page
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')       #this is a decorator to make sure a user that is not logged in won't access this page
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {
        'form':form,
    }
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')       #this is a decorator to make sure a user that is not logged in won't access this page
@admin_only                              #this is a decorator to make sure only admins access this page
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers':customers, 'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}

    return render(request, 'accounts/home.html', context)

@login_required(login_url='login')            #this is a decorator to make sure a user that is not logged in won't access this page
@allowed_users(allowed_roles=['admin'])      #this is a decorator to make sure only admins access this page
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])      #this is a decorator to make sure only admins access this page
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=Order.objects.all())

    context = {
        'orders':orders,
        'customer':customer,
        'total_orders':total_orders,
        'myFilter':myFilter,
    }

    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])      #this is a decorator to make sure only admins access this page
def createOrder(request, pk):
    OrderFormset = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=7)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormset(instance=customer)
    #form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        formset = OrderFormset(request.POST, instance=customer)
        if formset.is_valid:
            formset.save()
            return redirect('customer', pk)


    context = {
        'formset':formset
    }
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])      #this is a decorator to make sure only admins access this page
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {
        'form':form
    }
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])      #this is a decorator to make sure only admins access this page
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {
        'item': order
    }
    return render(request, 'accounts/delete_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])      #this is a decorator to make sure only admins access this page
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid:
            form.save()
            return redirect('customer', pk)
    context = {
        'form':form,
    }
    return render(request, 'accounts/update_customer.html', context)
