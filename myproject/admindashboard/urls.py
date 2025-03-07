# app/urls.py
from django.urls import path
from admindashboard.views import manage_users, add_customer, monitor_transactions, add_seller, manage_contents

urlpatterns = [
    path('manage_users/', manage_users, name='manage_users'),
    path('monitor_transactions/', monitor_transactions, name='monitor_transactions'),
    path('add_customer/', add_customer, name='add_customer'),
    path('add_seller/', add_seller, name='add_seller'),
    path('manage_contents/', manage_contents, name='manage_contents'),
]

    