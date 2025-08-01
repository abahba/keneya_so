# Generated by Django 5.2.2 on 2025-07-09 13:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_historiqueconsultation'),
        ('patients', '0005_historiquepatient_delete_patientlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='DossierMedical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('antecedents', models.TextField(blank=True)),
                ('allergies', models.TextField(blank=True)),
                ('traitements_chroniques', models.TextField(blank=True)),
                ('notes_supplementaires', models.TextField(blank=True)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dossier_medical', to='patients.patient')),
            ],
        ),
    ]
