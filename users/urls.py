# users/urls.py

from django.conf import settings
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views
from .views import (
    CustomLoginView, register, profile_view, edit_profile, 
    delete_profile, logout_view
)

app_name = 'users'

urlpatterns = [
    # 1. Autenticación: Login, Logout y Registro
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # 2. Perfil de Usuario
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-profile/', delete_profile, name='delete_profile'),

    # 3. Código QR del usuario
    path('qr/<uuid:qr_key>/', views.qr_data_view, name='qr_data'),

    # 4. Restablecimiento de Contraseña
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password/password_reset_form.html',
            email_template_name='password/password_reset_email.html',
            subject_template_name='password/password_reset_subject.txt',
            success_url=reverse_lazy('users:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]

# Sirviendo archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
