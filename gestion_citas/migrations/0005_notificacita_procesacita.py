# Generated by Django 3.0 on 2019-12-23 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_citas', '0004_auto_20191218_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificaCita',
            fields=[
                ('idNotificaCita', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('notifLastrun', models.DateTimeField(auto_now=True, verbose_name='Ultima fecha de notificación')),
                ('firstupdated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('lastupdated', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('modifiedby', models.CharField(blank=True, default='fixuUser', max_length=50, verbose_name='Modificado por')),
            ],
        ),
        migrations.CreateModel(
            name='ProcesaCita',
            fields=[
                ('idProcesaCita', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('procLastrun', models.DateTimeField(auto_now=True, verbose_name='Ultima fecha de procesamiento')),
                ('firstupdated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('lastupdated', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('modifiedby', models.CharField(blank=True, default='fixuUser', max_length=50, verbose_name='Modificado por')),
            ],
        ),
    ]
