
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from app.models import Customer, Seller, Order, Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render,  get_object_or_404
from app.forms import CustomUserCreationForm

@csrf_exempt
def manage_users(request):
    """Handles user management: displaying users and deactivating them via form submission."""
    
    if request.method == 'POST':

        user_id = request.POST.get('id')
        user_type = request.POST.get('type')

        if user_type == 'customer':
            customer = get_object_or_404(Customer, customer_id=user_id)
            customer.delete()
        elif user_type == 'seller':
            seller = get_object_or_404(Seller, seller_id=user_id)
            seller.delete()

    # GET request: Show active users
    customers = Customer.objects.all()
    sellers = Seller.objects.all()

    context = {
        'customers': customers,
        'sellers': sellers,
    }
    return render(request, 'app/manage_users.html', context)

def add_customer(request):
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
                return manage_users(request)
    else:
        form = UserCreationForm()
    return render(request, 'app/add_customer.html', {'form': form})

@csrf_protect
def add_seller(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Seller.objects.create(
                seller_id=user.username,
                name=request.POST['name'],
                email=user.email,
                phone=request.POST['phone'],
                address=request.POST['address']
            )
            return manage_users(request)
    else:
        form = UserCreationForm()
    return render(request, 'app/add_seller.html', {'form': form})

@csrf_exempt
def manage_contents(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, item_id=item_id)
        item.delete()

    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request,'app/manage_contents.html',context)

def monitor_transactions(request):
    orders = Order.objects.all()

    context = {
        'orders': orders,
    }
    return render(request, 'app/monitor_transactions.html', context) 

@staff_member_required
def admin_dashboard(request):
    return render(request, 'admindashboard/admin_dashboard.html')
