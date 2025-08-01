# Generated by Django 5.2.2 on 2025-07-04 22:11

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_dossier', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('sexe', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=10)),
                ('telephone', models.CharField(blank=True, max_length=15, null=True)),
                ('adresse', models.TextField(blank=True, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
