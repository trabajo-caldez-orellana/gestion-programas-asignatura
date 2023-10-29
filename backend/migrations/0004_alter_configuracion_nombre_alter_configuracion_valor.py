# Generated by Django 4.2.4 on 2023-10-22 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_rename_version_plan_asignatura_programatieneactividadreservada_version_programa_asignatura_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracion',
            name='nombre',
            field=models.CharField(choices=[('IPM', 'Días previos al inicio del Semestre para Modificar el Programa'), ('IPV', 'Días previos al inicio del Semestre para Validar el Programa'), ('IPC', 'Días previos al inicio del Semestre para Corregir el Programa')], max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='valor',
            field=models.IntegerField(),
        ),
    ]
