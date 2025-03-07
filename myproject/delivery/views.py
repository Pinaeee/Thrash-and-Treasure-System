from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Courier, Shipping, Issues, DeliveryReport
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Q

# DASHBOARD
@login_required
def delivery_dashboard(request):
    """Renders the delivery coordinator dashboard."""
    return render(request, 'delivery/dashboard.html', {'title': 'Delivery Dashboard'})

# ASSIGN COURIERS
@login_required
def assign_couriers(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        courier_id = request.POST.get('courier_id')

        try:
            shipping = get_object_or_404(Shipping, order_id=order_id)
            courier = get_object_or_404(Courier, courier_id=courier_id)
        except Exception as e:
            messages.error(request, "Error: Selected order or courier not found.")
            return redirect('delivery:del_couriers')
       
        shipping.courier_id = courier
        shipping.shipping_status = "Assigned"
        shipping.save()

        courier.status = "Busy"
        courier.save()
        
        messages.success(request, "Courier successfully assigned.")
        return redirect('delivery:del_couriers')

    unassigned_deliveries = Shipping.objects.filter(order__order_status="Accepted", shipping_status='Unassigned').select_related('order')
    available_couriers = Courier.objects.filter(status="Available")

    return render(request, 'delivery/del_couriers.html', {
        'unassigned_deliveries': unassigned_deliveries,
        'available_couriers': available_couriers,
        'title': 'Assign Couriers',
    })


# TRACK DELIVERIES
@login_required
def track_deliveries(request):
   
    deliveries = Shipping.objects.exclude(Q(shipping_status="Delivered") | Q(shipping_status="Unassigned")) # Exclude delivered & unassigned orders 

    # Example: Adding longitude and latitude for demo purposes
    for delivery in deliveries:
        delivery.longitude = 101.6964  # Replace with actual longitude
        delivery.latitude = 2.9264  # Replace with actual latitude

    return render(request, 'delivery/del_deliveries.html', {
        'deliveries': deliveries,
        'title': 'Track Deliveries',
    })

def update_status(request, shipping_id): # Delivery status
    shipping = get_object_or_404(Shipping, shipping_id=shipping_id)

    if request.method == "POST":
        new_status = request.POST.get("shipping_status")
        if new_status in ["Shipped", "Delivered"]:
            shipping.shipping_status = new_status
            shipping.save()
            messages.success(request, f"Order {shipping.order.order_id} is {new_status}.")

        return redirect("delivery:track_deliveries")


# HANDLE ISSUES
@login_required
def handle_issues(request):
    if request.method == "POST":

        issue_id = request.POST.get("issue_id")
        resolution_status = request.POST.get("resolution_status")
        resolution_description = request.POST.get("resolution_description")

        issue = get_object_or_404(Issues, issue_id=issue_id)
        issue.issue_status = resolution_status
        issue.issue_description = resolution_description
        issue.save()

        return redirect("delivery:del_issues")

    pending_issues = Issues.objects.filter(order__order_status="Accepted", issue_status="Pending")

    return render(request, "delivery/del_issues.html", {
        "pending_issues": pending_issues,
        "title": "Handle Issues"
    })


# GENERATE REPORT
@login_required
def generate_report(request):
    if request.method == "POST":
        report_type = request.POST.get("report_type", "Daily")

        now = datetime.now()
        if report_type == "Daily":
            start_date = now - timedelta(days=1)
        elif report_type == "Weekly":
            start_date = now - timedelta(weeks=1)
        elif report_type == "Monthly":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=1)  # Default to daily

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = now.strftime("%Y-%m-%d")

        # Fetch data based on selected time range
        total_deliveries = Shipping.objects.filter(order__order_date__gte=start_date).count()
        successful_deliveries = Shipping.objects.filter(
            shipping_status="Delivered", order__order_date__gte=start_date
        ).count()
        pending_deliveries = Shipping.objects.filter(
            shipping_status="Assigned", order__order_date__gte=start_date
        ).count()
        issues_reported = Issues.objects.filter(order__order_date__gte=start_date).count()

        message = "No reports available for this period." if total_deliveries == 0 else None

        context = {
            "report_type": report_type,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "total_deliveries": total_deliveries,
            "successful_deliveries": successful_deliveries,
            "pending_deliveries": pending_deliveries,
            "issues_reported": issues_reported,
            "message": message,
            "title": "Generate Report",
        }
        return render(request, "delivery/del_report.html", context)

    return render(request, "delivery/del_report.html", {"message": "Select a report type to generate."})


def save_report(request): # Save report to database
    if request.method == "POST":
        
        DeliveryReport.objects.create(
            report_date=datetime.now().date(),
            report_type=request.POST.get("report_type"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            total_deliveries=request.POST.get("total_deliveries"),
            successful_deliveries=request.POST.get("successful_deliveries"),
            pending_deliveries=request.POST.get("pending_deliveries"),
            issues_reported=request.POST.get("issues_reported"),
        )
        return redirect("delivery:del_report")

    return redirect("delivery:del_report")