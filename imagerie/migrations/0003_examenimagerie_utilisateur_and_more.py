# Generated by Django 5.2.2 on 2025-07-16 08:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagerie', '0002_historiqueimagerie'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='examenimagerie',
            name='utilisateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='examens_enregistres', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='examenimagerie',
            name='prescripteur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='examens_prescrits', to=settings.AUTH_USER_MODEL),
        ),
    ]
