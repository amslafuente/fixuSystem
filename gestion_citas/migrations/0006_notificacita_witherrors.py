# Generated by Django 3.0.1 on 2019-12-29 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_citas', '0005_notificacita_procesacita'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacita',
            name='witherrors',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Con errores'),
        ),
    ]
