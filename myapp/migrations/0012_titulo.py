# Generated by Django 5.0.6 on 2024-06-03 02:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_empleado_horaextradia_empleado_horaextranoche'),
    ]

    operations = [
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('nombre_especialidad', models.CharField(max_length=100)),
                ('institucion', models.CharField(max_length=100)),
                ('anio_titulacion', models.IntegerField()),
                ('empleado', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='titulos', to='myapp.empleado')),
            ],
        ),
    ]