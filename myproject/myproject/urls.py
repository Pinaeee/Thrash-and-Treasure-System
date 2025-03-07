"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from app import views as main_views
from cart import views as cart_views
from admindashboard import views as admin_views
import django.contrib.auth.views
from seller import views as seller_views
from checkout import views as checkout_views
from delivery import views as delivery_views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from app.views import custom_login, admin_dashboard
from checkout.views import checkout, process_checkout
from app.views import signup, signup_customer, signup_seller
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', main_views.home, name='home'),
    
    re_path(r'^admin$', main_views.admin, name='administrator'),
    re_path(r'^login/$', custom_login, name='login'),
    re_path(r'^logout$',
        LogoutView.as_view(template_name = 'app/index.html'),
        name='logout'),
    re_path(r'^menu$', main_views.menu, name='menu'),

    re_path(r'^cart$', cart_views.cart, name='cart'),
    re_path(r'^add_to_cart/(?P<item_id>[^/]+)$', cart_views.add_to_cart, name='add_to_cart'),
    re_path(r'^remove_from_cart$', cart_views.remove_from_cart, name='remove_from_cart'),
    re_path(r'^managecartform$', cart_views.managecartform, name='managecartform'),

    re_path(r'^manage_users$', admin_views.manage_users, name='manage_users'),
    re_path(r'^manage_contents$', admin_views.manage_contents, name='manage_contents'),
    re_path(r'^monitor_transactions$', admin_views.monitor_transactions, name='monitor_transactions'),
    re_path(r'^admin_dashboard$', admin_dashboard, name='admin_dashboard'),
    re_path(r'^add_seller/$', admin_views.add_seller, name='add_seller'),
    re_path(r'^add_customer/$', admin_views.add_customer, name='add_customer'),


    re_path('dashboard/', main_views.dashboard, name='dashboard'),
    re_path('viewprofile/', seller_views.viewprofile, name='viewprofile'),
    re_path('editprofile/', seller_views.editprofile, name='editprofile'),
    re_path('product/', seller_views.product, name='product'),
    re_path('orders/', seller_views.orders, name='orders'),
    path("remove/<str:item_id>/", seller_views.remove, name="remove"),
    path('update_order_status/<str:order_id>/<str:status>/', seller_views.update_order_status, name='update_order_status'),
    path('generate_unique_item_id/<str:item_id>/', seller_views.generate_unique_item_id, name='generate_unique_item_id'),
    re_path('test/', seller_views.test, name='test'),
    path('love/<str:item_id>/', seller_views.love, name='love'),
    re_path(r'^seller_dashboard$', seller_views.dashboard, name='seller_dashboard'),

    path('checkout/', checkout_views.checkout, name='checkout'),
    path('process_checkout/', checkout_views.process_checkout, name='process_checkout'),

    re_path(r'^signup/$', signup, name='signup'),
    re_path(r'^signup/customer/$', signup_customer, name='signup_customer'),
    re_path(r'^signup/seller/$', signup_seller, name='signup_seller'),

    # DELIVERY
    re_path(r'^delivery_dashboard$', delivery_views.delivery_dashboard, name='delivery_dashboard'),

    path('assign/', delivery_views.assign_couriers, name='del_couriers'),
    path('track/', delivery_views.track_deliveries, name='track_deliveries'),
    path('update_status/<str:shipping_id>/', delivery_views.update_status, name='update_status'),
    path('handle_issues/', delivery_views.handle_issues, name='del_issues'),
    path("report/", delivery_views.generate_report, name="del_report"),
    path("save_report/", delivery_views.save_report, name="save_report"),

    path('delivery/', include('delivery.urls', namespace='delivery')),
]
