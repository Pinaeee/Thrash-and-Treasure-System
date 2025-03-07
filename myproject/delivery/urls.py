from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('assign/', views.assign_couriers, name='del_couriers'),
    path('track/', views.track_deliveries, name='track_deliveries'),
    path('update_status/<str:shipping_id>/', views.update_status, name='update_status'),
    path('handle_issues/', views.handle_issues, name='del_issues'),
    path("report/", views.generate_report, name="del_report"),
    path("save_report/", views.save_report, name="save_report"),
    path('', views.delivery_dashboard, name='delivery_dashboard'),
]
