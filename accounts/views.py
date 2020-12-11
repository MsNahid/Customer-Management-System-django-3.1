from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from . models import *
from .forms import OrderForm
from .filters import OrderFilter


# Create your views here.
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

def products(request):
    list_of_products = Product.objects.all()
    products = {'products' : list_of_products }
    return render(request, 'accounts/products.html', products)

def customer(request, request_id):
    customer = Customer.objects.get(id=request_id)
    orders = customer.order_set.all()
    num_of_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {"customer": customer, "orders": orders, "num_of_orders": num_of_orders, 'myFilter': myFilter }
    return render(request, 'accounts/customer.html', context)


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


def deleteOrder(request, request_id):
    order = Order.objects.get(id=request_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
    
