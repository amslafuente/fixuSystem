# Generated by Django 3.0 on 2019-12-22 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_clinica', '0014_equipamiento_stockratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamiento',
            name='stockratio',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
