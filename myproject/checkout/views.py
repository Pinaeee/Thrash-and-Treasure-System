from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils.crypto import get_random_string
from app.models import Order, Payment, Cart, Customer, Item
from datetime import datetime

def checkout(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        cart_items = Cart.objects.filter(cart_id__in=selected_items)
        total_amount = sum(item.total_price for item in cart_items)
        return render(request, 'app/checkout.html', {'cart_items': cart_items, 'total_amount': total_amount})
    return redirect('cart')

@require_POST
def process_checkout(request):
    user = request.user
    customer = Customer.objects.get(customer_id=user.username)
    selected_items = request.POST.getlist('selected_items')
    cart_items = Cart.objects.filter(cart_id__in=selected_items)
    
    # Store item details before deleting
    item_details = [{
        'name': item.product_id.item_name,
        'image': item.product_id.image_url,
        'quantity': item.quantity_purchase,
        'price': item.total_price
    } for item in cart_items]
    
    # Create a new order
    order = Order.objects.create(
        order_id=get_random_string(10),
        customer_id=customer,
        order_date=datetime.now(),
        order_status='Pending'
    )
    
    # Create a new payment
    payment = Payment.objects.create(
        payment_id=get_random_string(10),
        order_id=order,
        payment_amount=sum(item['price'] for item in item_details),
        payment_method=request.POST['payment_method'],
        payment_date=datetime.now(),
        payment_status='Completed'
    )
    
    # Clear the selected items from the cart
    cart_items.delete()
    
    # Generate the receipt
    receipt = {
        'order_id': order.order_id,
        'items': item_details,
        'total_amount': payment.payment_amount
    }
    
    return render(request, 'app/receipt.html', {'receipt': receipt})
