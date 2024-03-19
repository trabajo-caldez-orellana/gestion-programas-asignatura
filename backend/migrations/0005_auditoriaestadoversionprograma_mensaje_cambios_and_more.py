# Generated by Django 4.2.4 on 2024-03-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_asignatura_horas_evaluacion_rol_dedicacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditoriaestadoversionprograma',
            name='mensaje_cambios',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auditoriaestadoversionprograma',
            name='estado',
            field=models.CharField(choices=[('A', 'Aprbado'), ('PC', 'Pedir cambios'), ('AD', 'Aprobacion Deprecada')], max_length=2),
        ),
    ]