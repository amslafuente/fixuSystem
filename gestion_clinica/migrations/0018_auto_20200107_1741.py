# Generated by Django 3.0.2 on 2020-01-07 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestion_clinica', '0017_auto_20191226_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='oto_Profesional',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='usuarios', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profesional',
            name='picturefile',
            field=models.ImageField(blank=True, upload_to='profesionales/'),
        ),
    ]
