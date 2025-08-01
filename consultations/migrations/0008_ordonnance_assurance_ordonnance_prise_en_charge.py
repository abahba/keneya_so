# Generated by Django 5.2.4 on 2025-07-10 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assurances', '0002_historiqueassurance'),
        ('consultations', '0007_servicehospitalier_hospitalisation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordonnance',
            name='assurance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assurances.assurance'),
        ),
        migrations.AddField(
            model_name='ordonnance',
            name='prise_en_charge',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assurances.priseencharge'),
        ),
    ]
