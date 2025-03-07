from django.db import models
from app.models import Order
from datetime import datetime


class Courier(models.Model):
    courier_id = models.CharField(max_length=10, primary_key=True) 
    dp_name = models.CharField(max_length=100)  # Delivery person name
    dp_phone_number = models.CharField(max_length=15)  # Phone number
    courier_company = models.CharField(max_length=50, default="Unknown")
    status = models.CharField(
        max_length=20,
        choices=[('Available', 'Available'), ('Busy', 'Busy')],
        default='Available'
    ) 

    def __str__(self):
        return f"{self.dp_name} ({self.courier_id}) - {self.courier_company} - {self.status}"
    

class Shipping(models.Model):
    SHIPPING_STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('Unassigned', 'Unassigned'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    shipping_id = models.CharField(max_length=20, primary_key=True) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True) 
    shipping_status = models.CharField(max_length=20, choices=SHIPPING_STATUS_CHOICES, default="Unassigned")  

    def __str__(self):
        return f"Shipping {self.shipping_id} - {self.shipping_status}"



class Issues(models.Model):
    ISSUE_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Resolved", "Resolved"),
        ("Escalated", "Escalated"),
    ]

    issue_id = models.CharField(max_length=10, primary_key=True) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    issue_description = models.TextField() 
    issue_status = models.CharField(max_length=20, choices=ISSUE_STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"Issue {self.issue_id} - {self.issue_status}"


class DeliveryReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_date = models.DateField(default=datetime.now)  # Report generation date
    report_type = models.CharField(max_length=10)  # Daily, Weekly, Monthly
    start_date = models.DateField()  # Time range start
    end_date = models.DateField()  # Time range end
    total_deliveries = models.IntegerField(default=0)
    successful_deliveries = models.IntegerField(default=0)
    pending_deliveries = models.IntegerField(default=0)
    issues_reported = models.IntegerField(default=0)

    def __str__(self):
        return f"Report {self.report_id} ({self.report_type})"
