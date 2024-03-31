# Generated by Django 4.2.4 on 2024-03-31 13:00

import backend.common.funciones_fecha
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auditoriaestadoversionprograma_mensaje_cambios_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditoriaRevisionDocentes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modificado_en', models.DateTimeField(default=backend.common.funciones_fecha.obtener_fecha_y_hora_actual)),
                ('accion', models.CharField(choices=[('CN', 'Crear nuevo programa de asignatura'), ('E', 'Editar programa de asignatura'), ('P', 'Presentar programa de asignatura para aprobación'), ('A', 'Aprobar programa de asignatura')], max_length=2)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='backend.rol')),
                ('version_programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.versionprogramaasignatura')),
            ],
            options={
                'verbose_name_plural': 'Auditorias Revisión de Docentes',
            },
        ),
    ]
