from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from .models import AnalyseBiologique, ResultatAnalyse, HistoriqueAnalyse
from .forms import AnalyseBiologiqueForm, ResultatAnalyseForm
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json
from django.contrib import messages
from .forms import AnalyseBiologiqueForm
from .models import TypeAnalyse, HistoriqueAnalyse
from consultations.models import Consultation

# 📄 Liste des analyses
@login_required
def liste_analyses(request):
    analyses = AnalyseBiologique.objects.select_related('patient', 'type_analyse').order_by('-date_demande')

    search = request.GET.get('search')
    if search:
        analyses = analyses.filter(
            patient__nom__icontains=search
        ) | analyses.filter(
            patient__prenom__icontains=search
        )

    return render(request, 'laboratoire/liste_analyses.html', {'analyses': analyses})


# ➕ Ajouter une analyse
@login_required
def ajouter_analyse(request):
    if request.method == 'POST':
        form = AnalyseBiologiqueForm(request.POST)
        if form.is_valid():
            analyse = form.save(commit=False)

            # ✅ Créer un nouveau type d’analyse si nécessaire
            if not analyse.type_analyse and analyse.autre_type_analyse:
                nouveau_type, created = TypeAnalyse.objects.get_or_create(nom=analyse.autre_type_analyse)
                analyse.type_analyse = nouveau_type

            # ✅ Ajout des champs liés
            analyse.date_prescription = timezone.now()
            analyse.utilisateur = request.user
            analyse.save()

            # ✅ Historique
            HistoriqueAnalyse.objects.create(
                analyse=analyse,
                action='ajout',
                utilisateur=request.user,
                description=f"Ajout de l'analyse pour {analyse.patient}"
            )

            messages.success(request, "✅ Analyse ajoutée avec succès.")
            return redirect('liste_analyses')
        else:
            messages.error(request, "❌ Erreur lors de l'ajout de l’analyse.")
    else:
        form = AnalyseBiologiqueForm()

    return render(request, 'laboratoire/ajouter_analyse.html', {'form': form})


# 📝 Modifier une analyse (optionnel)
@login_required
def modifier_analyse(request, analyse_id):
    analyse = get_object_or_404(AnalyseBiologique, id=analyse_id)
    if request.method == 'POST':
        form = AnalyseBiologiqueForm(request.POST, instance=analyse)
        if form.is_valid():
            form.save()
            return redirect('liste_analyses')
    else:
        form = AnalyseBiologiqueForm(instance=analyse)
    return render(request, 'laboratoire/modifier_analyse.html', {'form': form})


# 🔬 Ajouter un résultat d’analyse
@login_required
def ajouter_resultat(request, analyse_id):
    analyse = get_object_or_404(AnalyseBiologique, id=analyse_id)
    if request.method == 'POST':
        form = ResultatAnalyseForm(request.POST)
        if form.is_valid():
            resultat = form.save(commit=False)
            resultat.analyse = analyse
            resultat.date_resultat = timezone.now()
            resultat.utilisateur = request.user
            resultat.save()

            HistoriqueAnalyse.objects.create(
                analyse=analyse,
                action='modification',
                utilisateur=request.user,
                description=f"Ajout ou modification du résultat"
            )

            messages.success(request, f"🧪 Résultat ajouté pour {analyse.patient}.")
            return redirect('detail_analyse', analyse_id=analyse.id)
        else:
            messages.error(request, "❌ Erreur lors de l'ajout du résultat.")
    else:
        form = ResultatAnalyseForm()
    return render(request, 'laboratoire/ajouter_resultat.html', {'form': form, 'analyse': analyse})


# 👁️ Voir le détail d’une analyse
@login_required
def detail_analyse(request, analyse_id):
    analyse = get_object_or_404(AnalyseBiologique, id=analyse_id)
    try:
        resultat = analyse.resultat
    except ResultatAnalyse.DoesNotExist:
        resultat = None
    return render(request, 'laboratoire/detail_analyse.html', {
        'analyse': analyse,
        'resultat': resultat
    })

def historique_analyse(request, analyse_id):
    analyse = get_object_or_404(AnalyseBiologique, id=analyse_id)
    historique = analyse.historiques.order_by('-date')
    return render(request, 'laboratoire/historique_analyse.html', {
        'analyse': analyse,
        'historique': historique
    })


@login_required
def export_analyses_pdf(request):
    analyses = AnalyseBiologique.objects.select_related('patient').order_by('-date_demande')
    template = get_template('laboratoire/export_analyses_pdf.html')
    html = template.render({'analyses': analyses})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="analyses.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

@login_required
def export_analyses_excel(request):
    analyses = AnalyseBiologique.objects.select_related('patient').order_by('-date_demande')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Analyses"

    ws.append(['Patient', 'Type d\'analyse', 'Date', 'Résultat'])

    for analyse in analyses:
        try:
            resultat = analyse.resultat.resultat  # champ "résultat" du modèle ResultatAnalyse
        except ResultatAnalyse.DoesNotExist:
            resultat = "En attente"

        ws.append([
            analyse.patient.nom_complet,
            analyse.type_analyse.nom,
            analyse.date_prescription.strftime('%d/%m/%Y %H:%M'),
            resultat
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="analyses.xlsx"'
    wb.save(response)
    return response

@login_required
def modifier_analyse(request, analyse_id):
    analyse = get_object_or_404(AnalyseBiologique, id=analyse_id)
    if request.method == 'POST':
        form = AnalyseBiologiqueForm(request.POST, instance=analyse)
        if form.is_valid():
            form.save()
            HistoriqueAnalyse.objects.create(
                analyse=analyse,
                action='modification',
                utilisateur=request.user,
                description=f"Modification de l'analyse pour {analyse.patient}"
            )
            return redirect('liste_analyses')
    else:
        form = AnalyseBiologiqueForm(instance=analyse)
    return render(request, 'laboratoire/modifier_analyse.html', {'form': form})

@login_required
def statistiques_analyses(request):
    analyses_par_mois = AnalyseBiologique.objects.annotate(
        mois=TruncMonth('date_prescription')
    ).values('mois').annotate(total=Count('id')).order_by('mois')

    labels = [a['mois'].strftime("%B") for a in analyses_par_mois]
    data = [a['total'] for a in analyses_par_mois]

    return render(request, 'laboratoire/statistiques_analyses.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })

@login_required
def prescrire_analyse_depuis_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    patient = consultation.patient

    if request.method == 'POST':
        form = AnalyseBiologiqueForm(request.POST)
        if form.is_valid():
            analyse = form.save(commit=False)
            analyse.consultation = consultation
            analyse.patient = patient
            analyse.utilisateur = request.user
            analyse.date_prescription = timezone.now()

            if not analyse.type_analyse and analyse.autre_type_analyse:
                type_analyse, created = TypeAnalyse.objects.get_or_create(nom=analyse.autre_type_analyse)
                analyse.type_analyse = type_analyse

            analyse.save()

            HistoriqueAnalyse.objects.create(
                analyse=analyse,
                action='ajout',
                utilisateur=request.user,
                description=f"Analyse prescrite depuis la consultation {consultation.id}"
            )

            messages.success(request, "✅ Analyse prescrite avec succès.")
            return redirect('detail_consultation', consultation_id=consultation.id)
        else:
            messages.error(request, "❌ Erreur lors de la prescription de l’analyse.")
    else:
        form = AnalyseBiologiqueForm()

    return render(request, 'laboratoire/prescrire_analyse_depuis_consultation.html', {
        'form': form,
        'consultation': consultation,
        'patient': patient,
    })

from facturation.models import Facture
from django.shortcuts import render

def factures_analyses(request):
    factures = Facture.objects.filter(analyse__isnull=False).select_related('patient', 'analyse')
    return render(request, 'facturation/factures_par_analyse.html', {
        'factures': factures
    })

