from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import os
import uuid
import qrcode
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Rol"))
    description = models.TextField(blank=True, verbose_name=_("Descripción"))

    class Meta:
        verbose_name = _("Rol")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.name


def unique_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('profile_pics', filename)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_("Correo electrónico"))
    documento = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Documento"))
    direccion = models.TextField(blank=True, null=True, verbose_name=_("Dirección"))
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Celular"))
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Rol"))
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name=_("Fecha de nacimiento"))
    grupo_sanguineo = models.CharField(max_length=5, blank=True, null=True, verbose_name=_("Grupo sanguíneo"))
    alergias = models.TextField(blank=True, null=True, verbose_name=_("Alergias"))
    enfermedades_cronicas = models.TextField(blank=True, null=True, verbose_name=_("Enfermedades crónicas"))
    discapacidades = models.TextField(blank=True, null=True, verbose_name=_("Discapacidades"))
    seguro_medico = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Seguro médico"))
    medico_principal = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Médico Principal"))
    centro_medico_principal = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Centro Médico Principal"))
    contacto_nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Nombre de Contacto"))
    contacto_numero = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Número de Contacto"))
    qr_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    foto_perfil = models.ImageField(upload_to="profile_pics/", blank=True, null=True, verbose_name="Foto de Perfil")

    def get_qr_url(self):
        """Devuelve la URL del código QR del usuario."""
        return reverse('users:qr_data', args=[self.qr_key])

    def regenerate_qr_code(self):
        """
        Método para regenerar el código QR del usuario.
        """
        base_url = "http://192.168.0.27:8000"
        qr_url = f"{base_url}{reverse('users:qr_data', args=[self.qr_key])}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_image.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        qr_file_name = f"{self.username}_qr.png"
        self.qr_code.save(qr_file_name, ContentFile(qr_buffer.getvalue()), save=False)

        # Asegúrate de guardar el objeto después de regenerar
        self.save()

def generate_qr_code(self):
    if not self.qr_key:
        self.qr_key = uuid.uuid4()

    base_url = "http://127.0.0.1:8000"
    qr_url = f"{base_url}{self.get_qr_url()}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    qr_file_name = f"qr_codes/{self.username}_qr.png"
    self.qr_code.save(qr_file_name, ContentFile(qr_buffer.getvalue()), save=False)

def save(self, *args, **kwargs):
    # Genera el QR antes de guardar el usuario
    if not self.qr_code:
        self.generate_qr_code()
    super().save(*args, **kwargs)

class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name=_("Usuario"))
    action = models.CharField(max_length=255, verbose_name=_("Acción"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha y hora"))

    class Meta:
        verbose_name = _("Registro de Actividad")
        verbose_name_plural = _("Registros de Actividad")

    def __str__(self):
        return f"{self.user.username if self.user else 'Desconocido'}: {self.action}"


class LogConfig(models.Model):
    LOG_PERIODS = [
        ('daily', _("Diario")),
        ('weekly', _("Semanal")),
        ('monthly', _("Mensual")),
        ('yearly', _("Anual")),
    ]
    period = models.CharField(max_length=10, choices=LOG_PERIODS, default='monthly', verbose_name=_("Período del log"))

    class Meta:
        verbose_name = _("Configuración del log")
        verbose_name_plural = _("Configuraciones del log")

    def __str__(self):
        return f"Configuración del log: {self.period}"
