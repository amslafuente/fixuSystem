# Generated by Django 3.0.2 on 2020-01-30 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_pacientes', '0001_initial'),
        ('gestion_citas', '0001_initial'),
        ('gestion_clinica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Antecedente',
            fields=[
                ('idAntecedente', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('familyproblems', models.TextField(blank=True, verbose_name='Antecedentes familiares')),
                ('prevsurgery', models.TextField(blank=True, verbose_name='Cirugías previas')),
                ('alergic', models.TextField(blank=True, verbose_name='Alergias')),
                ('otherpathol', models.TextField(blank=True, verbose_name='Otras patologías')),
                ('firstupdated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('lastupdated', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('modifiedby', models.CharField(blank=True, default='fixuUser', max_length=50, verbose_name='Modificado por')),
                ('oto_Paciente', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='antecedpaciente', to='gestion_pacientes.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('idConsulta', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('age', models.PositiveIntegerField(blank=True, verbose_name='Edad')),
                ('mass', models.PositiveIntegerField(blank=True, verbose_name='Peso (kg)')),
                ('height', models.PositiveIntegerField(blank=True, verbose_name='Altura (cm)')),
                ('physicalexplor', models.TextField(blank=True, verbose_name='Exploración física')),
                ('physicaltest', models.TextField(blank=True, verbose_name='Pruebas diagnósticas')),
                ('diagnostic', models.CharField(blank=True, max_length=250, verbose_name='Diagnóstico')),
                ('medicaltreatm', models.CharField(blank=True, max_length=250, verbose_name='Tratam. farmacológico')),
                ('physicaltreatm', models.CharField(blank=True, max_length=250, verbose_name='Tratam. físico')),
                ('prognosis', models.TextField(blank=True, verbose_name='Pronóstico')),
                ('picture1', models.ImageField(blank=True, upload_to='consultas/', verbose_name='Imagen 1')),
                ('picture2', models.ImageField(blank=True, upload_to='consultas/', verbose_name='Imagen 2')),
                ('picture3', models.ImageField(blank=True, upload_to='consultas/', verbose_name='Imagen 3')),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('firstupdated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('lastupdated', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('modifiedby', models.CharField(blank=True, default='fixuUser', max_length=50, verbose_name='Modificado por')),
                ('fk_Antecedente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='antecedentes', to='gestion_consultas.Antecedente')),
                ('fk_Paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paciente', to='gestion_pacientes.Paciente')),
                ('fk_Profesional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='profesional', to='gestion_clinica.Profesional')),
                ('oto_Cita', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='cita', to='gestion_citas.Cita')),
            ],
        ),
    ]
