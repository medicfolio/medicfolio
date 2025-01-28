# home/views.py 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Vista para el home/dashboard
def home_view(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')  # Redirige al dashboard si está autenticado
    return render(request, 'home/home.html')  # Redirige al home público si no está autenticado

# Vista del dashboard
@login_required
def dashboard_view(request):
    return render(request, 'home/dashboard.html')
