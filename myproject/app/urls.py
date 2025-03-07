from django.urls import path, include
from . import views
from admindashboard import views 

urlpatterns = [
    path('admin/', views.admin, name='admin_dashboard'),
    path('add_to_cart/<str:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('', include('admindashboard.urls')),
]

