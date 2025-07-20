# laboratoire/migrations/0007_remplir_date_demande.py
from django.db import migrations

def remplir_date_demande(apps, schema_editor):
    AnalyseBiologique = apps.get_model('laboratoire', 'AnalyseBiologique')
    for analyse in AnalyseBiologique.objects.all():
        analyse.date_demande = analyse.date_prescription
        analyse.save()

class Migration(migrations.Migration):
    dependencies = [
        ('laboratoire', '0006_rename_valeur_resultatanalyse_contenu_and_more'),  # Vérifiez le bon numéro
    ]
    
    operations = [
        migrations.RunPython(remplir_date_demande),
    ]

