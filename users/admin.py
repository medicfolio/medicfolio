from django.contrib import admin
from .models import CustomUser, Role, ActivityLog, LogConfig
from django.core.mail import send_mail
import csv
from django.http import HttpResponse


# Definir todas las acciones antes de registrarlas en los modelos
@admin.action(description='Regenerar códigos QR seleccionados')
def regenerate_qr_codes(modeladmin, request, queryset):
    for user in queryset:
        user.regenerate_qr_code()  # Llama al método para regenerar el QR
    modeladmin.message_user(request, "Los códigos QR se han regenerado correctamente.")


@admin.action(description='Eliminar usuarios seleccionados')
def delete_selected_users(modeladmin, request, queryset):
    queryset.delete()
    modeladmin.message_user(request, "Los usuarios seleccionados han sido eliminados correctamente.")


@admin.action(description='Desactivar usuarios seleccionados')
def deactivate_selected_users(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, "Los usuarios seleccionados han sido desactivados correctamente.")


@admin.action(description='Activar usuarios seleccionados')
def activate_selected_users(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, "Los usuarios seleccionados han sido activados correctamente.")


@admin.action(description='Resetear contraseñas de usuarios seleccionados')
def reset_passwords(modeladmin, request, queryset):
    for user in queryset:
        user.set_password('ContraseñaPredeterminada123')  # Cambia por una contraseña más segura
        user.save()
    modeladmin.message_user(request, "Las contraseñas de los usuarios seleccionados han sido restablecidas.")


@admin.action(description='Enviar notificación por correo')
def send_notification(modeladmin, request, queryset):
    for user in queryset:
        send_mail(
            'Notificación de MedicFolio',
            'Este es un mensaje automático para informarte de una actualización importante.',
            'soporte@medicfolio.com',
            [user.email],
            fail_silently=False,
        )
    modeladmin.message_user(request, "Las notificaciones se han enviado correctamente.")


@admin.action(description='Exportar usuarios seleccionados a CSV')
def export_users_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Nombre', 'Apellido', 'QR Key', 'Activo'])
    for user in queryset:
        writer.writerow([user.username, user.email, user.first_name, user.last_name, user.qr_key, user.is_active])

    return response


# Registro de modelos en el admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'qr_key', 'qr_code', 'is_active']
    search_fields = ['username', 'email']
    actions = [
        regenerate_qr_codes,
        delete_selected_users,
        deactivate_selected_users,
        activate_selected_users,
        reset_passwords,
        send_notification,
        export_users_to_csv,
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']  # Elimina la acción predeterminada de eliminación
        return actions


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp']
    search_fields = ['action', 'user__username']


@admin.register(LogConfig)
class LogConfigAdmin(admin.ModelAdmin):
    list_display = ['period']
