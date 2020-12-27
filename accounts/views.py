from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from . models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customers')
            user.groups.add(group)

            messages.success(request, "Account was created secuessfully by " + username)
            return redirect('/login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'username or password is incorrect!')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='accounts:login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all() 

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers': customers, 
                'orders': orders,
                'total_orders' : total_orders,
                'delivered': delivered,
                'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


def userPage(request):
    context ={}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    list_of_products = Product.objects.all()
    products = {'products' : list_of_products }
    return render(request, 'accounts/products.html', products)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def customer(request, request_id):
    customer = Customer.objects.get(id=request_id)
    orders = customer.order_set.all()
    num_of_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {"customer": customer, "orders": orders, "num_of_orders": num_of_orders, 'myFilter': myFilter }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, request_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    customer = Customer.objects.get(id=request_id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # print("print something: ", request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, request_id):
    order = Order.objects.get(id=request_id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # print("print something: ", request.POST)
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request,  'accounts/order_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, request_id):
    order = Order.objects.get(id=request_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
    
