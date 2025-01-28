# home/urls.py

from django.urls import path
from .views import home_view, dashboard_view
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),  # Página inicial que decide entre home o dashboard
    path('dashboard/', dashboard_view, name='dashboard'),  # Dashboard
]
