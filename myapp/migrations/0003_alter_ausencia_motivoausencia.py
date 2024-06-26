# Generated by Django 5.0.6 on 2024-05-27 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_solicitud_estadosolicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ausencia',
            name='motivoAusencia',
            field=models.CharField(choices=[('Enfermedad', 'Enfermedad'), ('Matrimonio', 'Matrimonio'), ('Mudanza', 'Mudanza'), ('Familiar', 'Nacimiento, fallecimiento, accidente o enfermedad grave de un familiar'), ('Deberes', 'Deberes inexcusables'), ('Prenatal', 'Exámenes prenatales o técnicas de preparación al parto'), ('Sindical', 'Funciones sindicales'), ('Nacimiento', 'Nacimiento de hijos, lactancia y relacionados'), ('Otros', 'Otros')], max_length=50),
        ),
    ]
