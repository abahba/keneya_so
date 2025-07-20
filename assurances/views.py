from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Assurance, PatientAssure, PriseEnCharge
from patients.models import Patient
from .forms import AssuranceForm, PatientAssureForm, PriseEnChargeForm
from xhtml2pdf import pisa
import openpyxl
from .models import HistoriqueAssurance

# === ASSURANCE ===
def liste_assurances(request):
    assurances = Assurance.objects.all()
    return render(request, 'assurances/liste_assurances.html', {'assurances': assurances})

def ajouter_assurance(request):
    if request.method == 'POST':
        form = AssuranceForm(request.POST)
        if form.is_valid():
            assurance = form.save()
            HistoriqueAssurance.objects.create(
                utilisateur=request.user,
                action="ajout",
                objet="Assurance",
                description=f"Ajout de l'assurance {assurance.nom}"
            )
            return redirect('liste_assurances')
    else:
        form = AssuranceForm()
    return render(request, 'assurances/ajouter_assurance.html', {'form': form})


# === PATIENT ASSURÉ ===
def liste_patients_assures(request):
    patients_assures = PatientAssure.objects.select_related('patient', 'assurance').all()
    return render(request, 'assurances/liste_patients_assures.html', {'patients_assures': patients_assures})

def ajouter_patient_assure(request):
    if request.method == 'POST':
        form = PatientAssureForm(request.POST)
        if form.is_valid():
            pa = form.save()
            HistoriqueAssurance.objects.create(
                utilisateur=request.user,
                action="ajout",
                objet="PatientAssure",
                description=f"Liaison de {pa.patient} à l'assurance {pa.assurance}"
            )
            return redirect('liste_patients_assures')
    else:
        form = PatientAssureForm()
    return render(request, 'assurances/ajouter_patient_assure.html', {'form': form})


# === PRISE EN CHARGE ===
def liste_prises_en_charge(request):
    query = request.GET.get('q')
    prises = PriseEnCharge.objects.select_related('patient', 'assurance')

    if query:
        prises = prises.filter(
            patient__nom__icontains=query
        ) | prises.filter(
            assurance__nom__icontains=query
        )

    return render(request, 'assurances/liste_prises_en_charge.html', {
        'prises': prises,
        'query': query,
    })

def ajouter_prise_en_charge(request):
    if request.method == 'POST':
        form = PriseEnChargeForm(request.POST)
        if form.is_valid():
            pc = form.save()
            HistoriqueAssurance.objects.create(
                utilisateur=request.user,
                action="ajout",
                objet="PriseEnCharge",
                description=f"Prise en charge de {pc.patient} par {pc.assurance} - Montant: {pc.montant_demande} FCFA"
            )
            return redirect('liste_prises_en_charge')
    else:
        form = PriseEnChargeForm()
    return render(request, 'assurances/ajouter_prise_en_charge.html', {'form': form})

# === EXPORT PDF ===
def export_prises_pdf(request):
    prises = PriseEnCharge.objects.select_related('patient', 'assurance').all()
    template = get_template('assurances/export_prises_pdf.html')
    html = template.render({'prises': prises})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prises_en_charge.pdf"'
    
    # Gestion des erreurs de génération PDF
    result = pisa.CreatePDF(html, dest=response)
    if result.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    
    return response

# === EXPORT EXCEL ===
def export_prises_excel(request):
    prises = PriseEnCharge.objects.select_related('patient', 'assurance').all()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prises en charge"
    ws.append(['Patient', 'Assurance', 'Montant demandé', 'Statut'])

    for p in prises:
        nom_patient = p.patient.nom_complet() if hasattr(p.patient, 'nom_complet') else str(p.patient)
        ws.append([
            nom_patient,
            p.assurance.nom,
            p.montant_demande,
            p.statut
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="prises_en_charge.xlsx"'
    wb.save(response)
    return response

def historique_assurances(request):
    historiques = HistoriqueAssurance.objects.select_related('utilisateur').order_by('-date')
    return render(request, 'assurances/historique_assurances.html', {'historiques': historiques})

from django.http import HttpResponse

def accueil_assurances(request):
    return HttpResponse("✅ Bienvenue dans l'app Assurances")
