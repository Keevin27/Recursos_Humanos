# Generated by Django 5.0.6 on 2024-05-28 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_solicitud_estadosolicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='estadoSolicitud',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('denegada', 'Denegada')], default='revision', max_length=9),
        ),
    ]