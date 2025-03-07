from django.contrib import admin
from app.models import Item, Seller, Customer, Cart, Order, Payment
from delivery.models import Courier, Shipping, Issues, DeliveryReport
admin.site.register(Item)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(Shipping)
admin.site.register(Issues)
admin.site.register(DeliveryReport)