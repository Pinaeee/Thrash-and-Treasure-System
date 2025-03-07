from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpRequest
from datetime import datetime
from app.models import Seller, Item, Order, Payment 
from app.models import Item
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import re

@require_http_methods(["POST"])
def update_order_status(request, order_id, status):
    try:
        order = Order.objects.get(order_id=order_id)
        valid_statuses = ['Accepted', 'Rejected', 'In Process']
        
        if status in valid_statuses:
            order.order_status = status
            order.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
# Orders page
def orders(request):
    orders = Order.objects.all()
    for order in orders:
        order.payments_list = Payment.objects.filter(order_id=order.order_id)
    return render(request, 'app/orders.html', {
        'title': 'Orders',
        'orders': orders,
        'year': datetime.now().year
    })


# Seller dashboard
def dashboard(request):
    assert isinstance(request, HttpRequest)
    return render(
        request, 
        'app/dashboard.html',
        {
            'title':'dashboard',
            'year':datetime.now().year,
        }
    )

# View profile

def viewprofile(request):
    try:
        # Fetch the seller using the logged-in user's username as seller_id
        seller = Seller.objects.get(seller_id=request.user.username)
    except Seller.DoesNotExist:
        # Handle case where seller doesn't exist (redirect or error message)
        return redirect('dashboard')  # Adjust as needed
    
    return render(request, 'app/viewprofile.html', {'seller': seller})

# Edit profile page
def editprofile(request):
    try:
        seller = Seller.objects.get(seller_id=request.user.username)
    except Seller.DoesNotExist:
        return redirect('dashboard.html')  # Redirect if seller not found

    if request.method == "POST":
        seller.name = request.POST.get("name", seller.name)
        seller.address = request.POST.get("address", seller.address)
        seller.phone = request.POST.get("phone", seller.phone)
        seller.save()
        return redirect("viewprofile")  # Redirect after saving changes

    return render(request, "app/editprofile.html", {"seller": seller})

# Product page
def product(request):
    items = Item.objects.filter(seller_id=request.user.username)
    print([item.item_id for item in items])  # Debugging: Print item IDs in console
    return render(request, 'app/product.html', {
        'title': 'Product List',
        'year': datetime.now().year,
        'items': items,
    })

def createproduct(request):
    assert isinstance(request, HttpRequest)
    return render(
        request, 
        'app/createproduct.html',
        {
            'title':'dashboard',
            'year':datetime.now().year,
        }
    )


def remove(request, item_id):
    if request.method == "POST":
        try:
            # Fetch the item to delete
            item = get_object_or_404(Item, item_id=item_id)
            
            # Ensure the item belongs to the logged-in seller
            if item.seller_id.seller_id != request.user.username:  # Compare with seller_id from Seller model
                return HttpResponseForbidden("You are not allowed to delete this product.")

            # Delete the item
            item.delete()
            return redirect("product")
        except Exception as e:
            # Handle any exceptions
            return HttpResponseForbidden(str(e))
    return redirect("product")

def generate_unique_item_id():
    """Generate a new item_id in the format 'PRXX', where XX is an incremented number."""
    last_item = Item.objects.filter(item_id__startswith="PR").order_by("-item_id").first()
    
    if last_item:
        match = re.search(r'PR(\d+)', last_item.item_id)
        if match:
            next_id = int(match.group(1)) + 1  # Increment the number
        else:
            next_id = 1  # Default if no number found
    else:
        next_id = 1  # Start at PR01 if no items exist

    return f"PR{str(next_id).zfill(2)}"  # Ensure it's always 2 digits (PR01, PR02, ...)

def test(request):
    if request.method == "POST":
        # Retrieve data from the form
        item_name = request.POST.get("name")
        item_description = request.POST.get("description")
        product_price = request.POST.get("price")
        product_quantity = request.POST.get("quantity")
        image_url = request.POST.get("image_url")

        # Ensure all required fields are present
        if item_name and product_price and product_quantity:
            try:
                # Fetch the Seller instance using the logged-in user's username
                seller = Seller.objects.get(seller_id=request.user.username)

                # Create a new Item instance
                new_item = Item(
                    item_id=generate_unique_item_id(),  # Auto-generate item_id
                    item_name=item_name,
                    item_description=item_description,
                    product_price=product_price,
                    product_quantity=product_quantity,
                    image_url=image_url,
                    seller_id=seller  # ✅ Assign Seller instance, not string
                )
                new_item.save()  # Save to database
                return redirect("product")  # Redirect to product list

            except Seller.DoesNotExist:
                return HttpResponseForbidden("Seller not found")  # Handle missing seller

    return render(request, "app/test.html", {"title": "Create Product"})

def love(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    if request.method == "POST":
        # Update the item with the new data
        item.item_name = request.POST.get("item_name", item.item_name)
        item.image_url = request.POST.get("image", item.image_url)
        item.item_description = request.POST.get("item_description", item.item_description)
        item.product_quantity = request.POST.get("quantity", item.product_quantity)
        item.product_price = request.POST.get("price", item.product_price)
        item.save()
        return redirect("product")  # Redirect to the product list after saving

    return render(request, "app/love.html", {"item": item})