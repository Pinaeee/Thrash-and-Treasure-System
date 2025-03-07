from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Customer, Seller, Item, Cart, Order
from delivery.models import Shipping
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from .forms import CustomUserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    items = Item.objects.all()
    if request.user.is_authenticated:
        return redirect('/menu')
    else:
        return render(
            request,
            'app/index.html',
            {
                'title': 'Home Page',
                'year': datetime.now().year,
                'items': items,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Dr. Yeoh.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Thrash and Treasure System',
            'message':'This application processes ...',
            'year':datetime.now().year,
        }
    )

@login_required
def menu(request):
    user = request.user
    is_customer = Customer.objects.filter(customer_id=user.username).exists()
    is_seller = Seller.objects.filter(seller_id=user.username).exists()
    is_admin = user.is_superuser
    is_delivery_coordinator = user.groups.filter(name="Delivery Coordinator").exists()
    items = Item.objects.all()

    context = {
        'title': 'Main Menu',
        'is_customer': is_customer,
        'is_seller': is_seller,
        'is_admin': is_admin,
        'is_delivery_coordinator': is_delivery_coordinator,
        'year': datetime.now().year,
        'items': items,
    }
    context['user'] = user

    return render(request,'app/menu.html',context)

def admin(request):
    """Admin"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin.html',
        {
            'title':'Thrash and Treasure System',
            'message':'This application processes ...',
            'year':datetime.now().year,
        }
    )

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if Customer.objects.filter(customer_id=username).exists():
                return redirect('menu')
            elif Seller.objects.filter(seller_id=username).exists():
                return redirect('seller_dashboard')
            elif user.is_superuser:
                return redirect('admin_dashboard')
            elif user.groups.filter(name="Delivery Coordinator").exists():
                return redirect('delivery_dashboard') 
        else:
            return render(request, 'app/login.html', {'error': 'Invalid login credentials'})
    return render(request, 'app/login.html')

@login_required
def admin_dashboard(request):
    context = {
        'title': 'Admin Dashboard',
        'year': datetime.now().year,
    }
    return render(request, 'app/admin.html', context)

@login_required
def add_to_cart(request, item_id):
    user = request.user
    customer = Customer.objects.get(customer_id=user.username)
    item = Item.objects.get(item_id=item_id)
    
    cart_item, created = Cart.objects.get_or_create(
        customer_id=customer,
        product_id=item,
        defaults={'quantity_purchase': 1, 'total_price': item.product_price}
    )
    
    if not created:
        cart_item.quantity_purchase += 1
        cart_item.total_price += item.product_price
        cart_item.save()
    
    return redirect('cart')

@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')

def signup(request):
    return render(request, 'app/signup.html')

def signup_customer(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            if email and Customer.objects.filter(customer_email=email).exists():
                form.add_error('email', 'Email address already in use.')
            else:
                user = form.save()
                Customer.objects.create(
                    customer_id=user.username,
                    customer_name=request.POST['name'],
                    customer_email=email,
                    customer_phone=request.POST['phone'],
                    customer_address=request.POST['address']
                )
                auth_login(request, user)
                return redirect('menu')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/signup_customer.html', {'form': form})

@csrf_protect
def signup_seller(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            if email and Seller.objects.filter(email=email).exists():
                form.add_error('email', 'Email address already in use.')
            else:
                try:
                    user = form.save()
                    Seller.objects.create(
                        seller_id=user.username,
                        name=request.POST['name'],
                        email=user.email,
                        phone=request.POST['phone'],
                        address=request.POST['address']
                    )
                    auth_login(request, user)
                    return redirect('seller_dashboard')
                except IntegrityError:
                    form.add_error('email', 'Email address already in use.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/signup_seller.html', {'form': form})

# Automatic process (Accepted Order -> Shipping)
def process_accepted_orders():
    
    accepted_orders = Order.objects.filter(order_status="Accepted").exclude(
        order_id__in=Shipping.objects.values_list("order_id", flat=True)
    )

    for order in accepted_orders:
        # Create a new shipping entry with "Unassigned" status
        Shipping.objects.create(
            shipping_id="SP" + order.order_id[:5],
            order=order,
            courier=None, 
            shipping_status="Unassigned"
        )

    print(f"{accepted_orders.count()} new orders added to shipping.")

@receiver(post_save, sender=Order)
def auto_add_to_shipping(sender, instance, **kwargs):
    """Automatically adds accepted orders to shipping."""
    if instance.order_status == "Accepted":
        process_accepted_orders()