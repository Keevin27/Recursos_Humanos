# Generated by Django 5.0.6 on 2024-05-29 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_solicitud_estadosolicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='estadoSolicitud',
            field=models.CharField(default='revision', max_length=20),
        ),
    ]
