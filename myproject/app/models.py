"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import User

#sharing entity

class Seller(models.Model):
    seller_id = models.CharField(primary_key=True, max_length=10, default='DEFAULT_ID')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.TextField()
    item_description = models.TextField(null=True,default=None, blank=True)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE, default='DEFAULT_ID')
    product_price = models.FloatField(default=0.0)
    product_quantity = models.IntegerField(default=0)
    image_url = models.URLField(max_length=200, null=True, blank=True)

class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=10)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(unique=True)
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()

    def __str__(self):
        return str(self.customer_name)

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_purchase = models.IntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return str(self.cart_id)

class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=10)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    order_status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.order_id)

class Payment(models.Model):
    payment_id = models.CharField(primary_key=True, max_length=10)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField()
    payment_status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.payment_id)
