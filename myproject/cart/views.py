from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from datetime import datetime
from app.models import Cart, Customer, Item

@login_required
def cart(request):
    """Renders the cart page."""
    assert isinstance(request, HttpRequest)
    user = request.user
    customer = Customer.objects.get(customer_id=user.username)
    cart_items = Cart.objects.filter(customer_id=customer)
    
    if request.method == 'POST':
        for cart_item in cart_items:
            cart_item_id = cart_item.cart_id
            if f'update_quantity_{cart_item_id}' in request.POST:
                new_quantity = int(request.POST[f'quantity_{cart_item_id}'])
                cart_item.quantity_purchase = new_quantity
                cart_item.total_price = new_quantity * cart_item.product_id.product_price
                cart_item.save()
            elif f'delete_item_{cart_item_id}' in request.POST:
                cart_item.delete()
        return redirect('cart')
    
    return render(
        request,
        'app/cart.html',
        {
            'title': 'Your Cart',
            'year': datetime.now().year,
            'cart_items': cart_items,
        }
    )

@login_required
def add_to_cart(request, item_id):
    """Adds an item to the cart."""
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
def remove_from_cart(request):
    """Removes an item from the cart."""
    assert isinstance(request, HttpRequest)
    # Logic to remove item from the cart
    return redirect('cart')

@login_required
def managecartform(request):
    """Renders the manage cart form page."""
    assert isinstance(request, HttpRequest)
    # Logic to manage cart form
    return render(
        request,
        'app/managecartform.html',
        {
            'title':'Manage Cart',
            'year': datetime.now().year,
        }
    )
