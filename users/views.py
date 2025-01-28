from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib import messages
from django.contrib.auth import logout
from .models import CustomUser, Role
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import get_messages

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home:dashboard')

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # No guardamos aún
            user.save()  # Llama al método `save` que genera el QR
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'users/profile.html', {"user": user})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu perfil ha sido eliminado.')
        return redirect('home:home')
    return render(request, 'users/delete_profile.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('home:home')

def qr_data_view(request, qr_key):
    user = get_object_or_404(CustomUser, qr_key=qr_key)
    return render(request, 'users/qr_data.html', {'user': user})

def get_qr_url(self):
    return reverse('users:qr_data', args=[self.qr_key])

@login_required
def home_view(request):
    return render(request, 'home.html')

def error_403(request, exception):
    return render(request, 'users/403.html', status=403)

def error_404(request, exception):
    return render(request, 'users/404.html', status=404)

def error_500(request):
    return render(request, 'users/500.html', status=500)

class MedicalInfoQRView(DetailView):
    model = CustomUser
    template_name = 'users/medical_info_qr.html'
    slug_field = 'qr_key'
    slug_url_kwarg = 'qr_key'
    
@login_required
def dashboard_view(request):
    return render(request, 'home/dashboard.html')

