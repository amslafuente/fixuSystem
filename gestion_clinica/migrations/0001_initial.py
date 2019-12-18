# Generated by Django 3.0 on 2019-12-17 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('idClinica', models.AutoField(primary_key=True, serialize=False)),
                ('dni', models.CharField(max_length=9, unique=True, verbose_name='DNI')),
                ('nif', models.CharField(blank=True, max_length=25, unique=True, verbose_name='NIF')),
                ('clinicname', models.CharField(max_length=100, verbose_name='Nombre clínica')),
                ('ownerfullname', models.CharField(max_length=100, verbose_name='Nombre titular')),
                ('numcolegiado', models.CharField(blank=True, max_length=25, unique=True, verbose_name='Número colegiado/a')),
                ('fulladdress', models.CharField(max_length=250, verbose_name='Dirección completa')),
                ('postcode', models.PositiveIntegerField(verbose_name='Código postal')),
                ('city', models.CharField(max_length=50, verbose_name='Ciudad')),
                ('province', models.CharField(blank=True, max_length=50, verbose_name='Provincia')),
                ('email', models.EmailField(max_length=50, verbose_name='Correo electrónico')),
                ('phone1', models.PositiveIntegerField(verbose_name='Teléfono principal')),
                ('phone2', models.PositiveIntegerField(blank=True, null=True, verbose_name='Teléfono alternativo')),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('picturefile', models.ImageField(blank=True, null=True, upload_to='clinica/', verbose_name='Archivo LOGO')),
                ('firstupdated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('lastupdated', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('modifiedby', models.CharField(blank=True, default='fixuUser', max_length=50, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Clínica',
                'verbose_name_plural': 'Clínicas',
            },
        ),
        migrations.CreateModel(
            name='Consultorio',
            fields=[
                ('idConsultorio', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('officeID', models.CharField(max_length=10, unique=True, verbose_name='Número/Identificación')),
                ('officeDesc', models.CharField(blank=True, max_length=100, verbose_name='Descripción')),
                ('officeIsavail', models.BooleanField(default=True, verbose_name='Disponible')),
                ('officeLocation', models.CharField(blank=True, max_length=50, verbose_name='Localización')),
                ('officeDepartment', models.CharField(blank=True, max_length=50, verbose_name='Departamento')),
                ('officeEquipment', models.TextField(blank=True, verbose_name='Equipamiento')),
                ('officePhone', models.PositiveIntegerField(blank=True, null=True, verbose_name='Teléfono consultorio')),
                ('officeNotes', models.TextField(blank=True, verbose_name='Notas')),
                ('firstupdated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('lastupdated', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('modifiedby', models.CharField(blank=True, default='fixuUser', max_length=50, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Consultorio',
                'verbose_name_plural': 'Consultorios',
                'ordering': ['idConsultorio'],
            },
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('oto_Profesional', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dni', models.CharField(max_length=9, unique=True, verbose_name='DNI')),
                ('nif', models.CharField(blank=True, max_length=25, verbose_name='NIF')),
                ('fullname', models.CharField(max_length=100, verbose_name='Nombre')),
                ('numcolegiado', models.CharField(blank=True, max_length=25, verbose_name='Número Colegiado/a')),
                ('position', models.CharField(max_length=100, verbose_name='Empleo/Puesto/Cargo')),
                ('department', models.CharField(blank=True, max_length=100, verbose_name='Departamento')),
                ('fulladdress', models.CharField(max_length=250, verbose_name='Dirección')),
                ('postcode', models.PositiveIntegerField(verbose_name='Cód. Postal')),
                ('city', models.CharField(max_length=50, verbose_name='Ciudad')),
                ('province', models.CharField(blank=True, max_length=50, verbose_name='Provincia')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='País')),
                ('email2', models.EmailField(max_length=50, verbose_name='Correo electrónico')),
                ('phone1', models.PositiveIntegerField(verbose_name='Teléfono principal')),
                ('phone2', models.PositiveIntegerField(blank=True, null=True, verbose_name='Teléfono alternativo')),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('currentstaff', models.BooleanField(default=True, verbose_name='En activo')),
                ('picturefile', models.ImageField(blank=True, upload_to='clinica/')),
                ('firstupdated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('lastupdated', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('modifiedby', models.CharField(blank=True, default='fixuUser', max_length=50, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Profesional',
                'verbose_name_plural': 'Profesionales',
                'ordering': ['oto_Profesional'],
            },
        ),
    ]