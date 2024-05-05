# Generated by Django 4.2.4 on 2024-05-05 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0009_versionprogramaasignatura_version_semestre_asignatura_ux"),
    ]

    operations = [
        migrations.AddField(
            model_name="rol",
            name="fecha_fin",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="rol",
            name="fecha_inicio",
            field=models.DateField(default="2024-01-01"),
            preserve_default=False,
        ),
    ]
