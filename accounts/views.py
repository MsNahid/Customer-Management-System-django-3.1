from django.shortcuts import render
from . models import *

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
    context = {"customer": customer, "orders": orders, "num_of_orders": num_of_orders }
    return render(request, 'accounts/customer.html', context)

    