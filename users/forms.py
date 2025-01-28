# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Role

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "role")  # Incluyendo 'role' directamente.

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name", "documento", "direccion", "celular", 
            "foto_perfil", "role", "fecha_nacimiento", "grupo_sanguineo", 
            "alergias", "enfermedades_cronicas", "discapacidades", "seguro_medico",
            "medico_principal", "centro_medico_principal", 
            "contacto_nombre", "contacto_numero"
        ]
        widgets = {
            'role': forms.Select(),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "documento": "Documento",
            "direccion": "Dirección",
            "celular": "Celular",
            "foto_perfil": "Foto de perfil",
            "role": "Rol",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "grupo_sanguineo": "Grupo Sanguíneo",
            "alergias": "Alergias",
            "enfermedades_cronicas": "Enfermedades Crónicas",
            "discapacidades": "Discapacidades",
            "seguro_medico": "Seguro Médico",
            "medico_principal": "Médico Principal",
            "centro_medico_principal": "Centro Médico Principal",
            "contacto_nombre": "Nombre de Contacto",
            "contacto_numero": "Número de Contacto",
        }
        help_texts = {
            "role": "Selecciona el rol del usuario, si corresponde.",
        }