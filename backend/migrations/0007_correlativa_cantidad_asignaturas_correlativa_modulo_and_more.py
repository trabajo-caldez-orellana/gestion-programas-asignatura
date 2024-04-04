# Generated by Django 4.2.4 on 2024-04-04 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auditoriarevisiondocentes'),
    ]

    operations = [
        migrations.AddField(
            model_name='correlativa',
            name='cantidad_asignaturas',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='correlativa',
            name='modulo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='correlativa',
            name='requisito',
            field=models.CharField(choices=[('asignatura', 'Asignatura aprobada o regular'), ('cantidad', 'Número de asignaturas aprobadas o regulares'), ('modulo', 'Módulo aprobado o regular')], default='asignatura', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='correlativa',
            name='asignatura_correlativa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='backend.asignatura'),
        ),
    ]