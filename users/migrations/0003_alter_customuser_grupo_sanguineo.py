# Generated by Django 5.1.5 on 2025-01-27 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='grupo_sanguineo',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Grupo sanguíneo'),
        ),
    ]
