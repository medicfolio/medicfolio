# home/urls.py

from django.urls import path
from .views import (
    dashboard_view,
    home_view,
    salon_clients,
    salon_clients_delete,
    salon_clients_detail,
    salon_data,
    salon_products,
    salon_products_delete,
    salon_products_detail,
    salon_transactions,
    salon_transactions_delete,
    salon_view,
)
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),  # Página inicial que decide entre home o dashboard
    path('dashboard/', dashboard_view, name='dashboard'),  # Dashboard
    path('salon/', salon_view, name='salon'),
    path('salon/api/data/', salon_data, name='salon_data'),
    path('salon/api/clients/', salon_clients, name='salon_clients'),
    path('salon/api/clients/<int:client_id>/', salon_clients_detail, name='salon_clients_detail'),
    path('salon/api/clients/<int:client_id>/delete/', salon_clients_delete, name='salon_clients_delete'),
    path('salon/api/products/', salon_products, name='salon_products'),
    path('salon/api/products/<int:product_id>/', salon_products_detail, name='salon_products_detail'),
    path('salon/api/products/<int:product_id>/delete/', salon_products_delete, name='salon_products_delete'),
    path('salon/api/transactions/', salon_transactions, name='salon_transactions'),
    path('salon/api/transactions/<int:transaction_id>/delete/', salon_transactions_delete, name='salon_transactions_delete'),
]
