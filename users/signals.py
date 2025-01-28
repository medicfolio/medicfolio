from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import MedicalProfile

@receiver(post_save, sender=CustomUser)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        instance.generate_qr()
        instance.save()