# Generated by Django 3.0.2 on 2020-01-12 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_pacientes', '0005_auto_20191228_1830'),
        ('gestion_consultas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consulta',
            name='oto_Paciente',
        ),
        migrations.AddField(
            model_name='consulta',
            name='fk_Paciente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='paciente', to='gestion_pacientes.Paciente'),
        ),
    ]
