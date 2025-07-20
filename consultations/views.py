from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Consultation, HistoriqueConsultation, DossierMedical
from .forms import ConsultationForm, DossierMedicalForm
from patients.models import Patient
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from .models import Ordonnance, LigneOrdonnance
from .forms import OrdonnanceForm, LigneOrdonnanceFormSet
from .models import Hospitalisation, ServiceHospitalier, HistoriqueHospitalisation
from .forms import HospitalisationForm
from django.utils import timezone
from django.utils.timezone import localtime
from django.db.models import Q  
from django.contrib import messages
from.forms import PrescriptionAnalyseForm
from .models import TypeAnalyse
from facturation.models import Facture
from django.shortcuts import render

# Liste des consultations (avec recherche)
@login_required
def liste_consultations(request):
    recherche = request.GET.get('recherche', '')
    consultations = Consultation.objects.select_related('patient')

    if recherche:
        consultations = consultations.filter(
            patient__nom__icontains=recherche
        )

    consultations = consultations.order_by('-date_consultation')
    return render(request, 'consultations/liste_consultations.html', {
        'consultations': consultations,
        'recherche': recherche
    })

# Ajouter une consultation
@login_required
def ajouter_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save()
            HistoriqueConsultation.objects.create(
                consultation=consultation,
                utilisateur=request.user,
                action='ajout',
                details='Consultation ajoutée.'
            )
            return redirect('liste_consultations')
    else:
        form = ConsultationForm()
    return render(request, 'consultations/ajouter_consultation.html', {'form': form})

# Modifier une consultation
@login_required
def modifier_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            HistoriqueConsultation.objects.create(
                consultation=consultation,
                utilisateur=request.user,
                action='modification',
                details='Consultation modifiée.'
            )
            return redirect('liste_consultations')
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'consultations/modifier_consultation.html', {'form': form})

# Supprimer une consultation
@login_required
def supprimer_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        HistoriqueConsultation.objects.create(
            consultation=consultation,
            utilisateur=request.user,
            action='suppression',
            details='Consultation supprimée.'
        )
        consultation.delete()
        return redirect('liste_consultations')
    return render(request, 'consultations/supprimer_consultation.html', {'consultation': consultation})

# Historique
@login_required
def historique_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    historiques = consultation.historiques.order_by('-date_action')
    return render(request, 'consultations/historique_consultation.html', {
        'consultation': consultation,
        'historiques': historiques
    })

@login_required
def export_historique_consultation_pdf(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    historiques = consultation.historiques.order_by('-date_action')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historique_consultation.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"Historique de la consultation - {consultation.patient}")

    y = 770
    for h in historiques:
        p.setFont("Helvetica", 10)
        text = f"{h.date_action.strftime('%d/%m/%Y %H:%M')} | {h.utilisateur} | {h.action} | {h.details}"
        p.drawString(40, y, text)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response

@login_required
def export_historique_consultation_excel(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    historiques = consultation.historiques.order_by('-date_action')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=historique_consultation.xlsx'

    wb = Workbook()
    ws = wb.active
    ws.title = "Historique"
    ws.append(["Date", "Utilisateur", "Action", "Détails"])

    for h in historiques:
        ws.append([
            h.date_action.strftime('%d/%m/%Y %H:%M'),
            str(h.utilisateur),
            h.action,
            h.details
        ])

    wb.save(response)
    return response

# Dossier médical
@login_required
def voir_dossier_medical(request, patient_id):
    dossier = DossierMedical.objects.filter(patient_id=patient_id).first()
    if not dossier:
        return redirect('creer_dossier_medical', patient_id=patient_id)
    return render(request, 'consultations/voir_dossier_medical.html', {'dossier': dossier})

@login_required
def creer_dossier_medical(request, patient_id):
    if DossierMedical.objects.filter(patient_id=patient_id).exists():
        return redirect('voir_dossier_medical', patient_id=patient_id)

    if request.method == 'POST':
        form = DossierMedicalForm(request.POST)
        if form.is_valid():
            dossier = form.save(commit=False)
            dossier.patient_id = patient_id
            dossier.auteur = request.user
            dossier.save()
            return redirect('voir_dossier_medical', patient_id=patient_id)
    else:
        form = DossierMedicalForm()
    return render(request, 'consultations/creer_dossier_medical.html', {'form': form})

@login_required
def modifier_dossier_medical(request, patient_id):
    dossier = get_object_or_404(DossierMedical, patient_id=patient_id)
    if request.method == 'POST':
        form = DossierMedicalForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            return redirect('voir_dossier_medical', patient_id=patient_id)
    else:
        form = DossierMedicalForm(instance=dossier)
    return render(request, 'consultations/modifier_dossier_medical.html', {'form': form, 'dossier': dossier})

@login_required
def creer_ordonnance(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    if request.method == 'POST':
        form = OrdonnanceForm(request.POST)
        formset = LigneOrdonnanceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            ordonnance = form.save(commit=False)
            ordonnance.consultation = consultation
            ordonnance.save()
            lignes = formset.save(commit=False)
            for ligne in lignes:
                ligne.ordonnance = ordonnance
                ligne.save()
            return redirect('voir_ordonnance', ordonnance.id)
    else:
        form = OrdonnanceForm()
        formset = LigneOrdonnanceFormSet()
    return render(request, 'consultations/creer_ordonnance.html', {
        'form': form,
        'formset': formset,
        'consultation': consultation
    })

@login_required
def voir_ordonnance(request, ordonnance_id):
    ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)
    return render(request, 'consultations/voir_ordonnance.html', {'ordonnance': ordonnance})

@login_required
def export_ordonnance_pdf(request, ordonnance_id):
    ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=ordonnance_{ordonnance.id}.pdf'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Ordonnance Médicale")

    p.setFont("Helvetica", 12)
    y = 770
    p.drawString(50, y, f"Patient : {ordonnance.consultation.patient.nom} {ordonnance.consultation.patient.prenom}")
    y -= 20
    p.drawString(50, y, f"Date : {ordonnance.date_creation.strftime('%d/%m/%Y %H:%M')}")
    y -= 20
    p.drawString(50, y, f"Assurance : {ordonnance.get_type_assurance_display()}")
    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Médicaments prescrits :")
    y -= 20

    p.setFont("Helvetica", 11)
    for ligne in ordonnance.lignes.all():
        p.drawString(60, y, f"- {ligne.medicament.nom} | {ligne.quantite} | {ligne.posologie} | {ligne.duree}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
            y -= 30
    if ordonnance.signature:
      p.setFont("Helvetica-Bold", 11)
      p.drawString(50, y, f"Signée par : {ordonnance.signature.get_full_name()}")

    p.showPage()
    p.save()
    return response

@login_required
def signer_ordonnance(request, ordonnance_id):
    ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)
    if request.method == 'POST':
        ordonnance.signature = request.user
        ordonnance.save()
        return redirect('voir_ordonnance', ordonnance_id=ordonnance.id)

@login_required
def liste_hospitalisations(request):
    recherche = request.GET.get('recherche', '')
    hospitalisations = Hospitalisation.objects.select_related('patient')

    if recherche:
        hospitalisations = hospitalisations.filter(
            Q(patient__nom__icontains=recherche) |
            Q(patient__prenom__icontains=recherche) |
            Q(service__icontains=recherche)
        )

    hospitalisations = hospitalisations.order_by('-date_entree')
    return render(request, 'consultations/liste_hospitalisations.html', {
        'hospitalisations': hospitalisations,
        'recherche': recherche
    })

@login_required
def ajouter_hospitalisation(request):
    if request.method == 'POST':
        form = HospitalisationForm(request.POST)
        if form.is_valid():
            hospitalisation = form.save()
            HistoriqueHospitalisation.objects.create(
                hospitalisation=hospitalisation,
                utilisateur=request.user,
                action='ajout',
                details='Hospitalisation ajoutée.'
            )
            return redirect('liste_hospitalisations')
    else:
        form = HospitalisationForm()
    return render(request, 'consultations/ajouter_hospitalisation.html', {'form': form})

@login_required
def modifier_hospitalisation(request, pk):
    hospitalisation = get_object_or_404(Hospitalisation, pk=pk)
    if request.method == 'POST':
        form = HospitalisationForm(request.POST, instance=hospitalisation)
        if form.is_valid():
            form.save()
            HistoriqueHospitalisation.objects.create(
                hospitalisation=hospitalisation,
                utilisateur=request.user,
                action='modification',
                details='Hospitalisation modifiée.'
            )
            return redirect('liste_hospitalisations')
    else:
        form = HospitalisationForm(instance=hospitalisation)
    return render(request, 'consultations/modifier_hospitalisation.html', {'form': form})

@login_required
def marquer_sortie_hospitalisation(request, pk):
    hospitalisation = get_object_or_404(Hospitalisation, pk=pk)
    
    # Vérifier si le patient n'est pas déjà sorti
    if hospitalisation.date_sortie:
        messages.warning(request, 'Ce patient est déjà sorti.')
        return redirect('liste_hospitalisations')
    
    if request.method == 'POST':
        hospitalisation.date_sortie = timezone.now()
        hospitalisation.save()
        
        HistoriqueHospitalisation.objects.create(
            hospitalisation=hospitalisation,
            utilisateur=request.user,
            action='sortie',
            details='Patient sorti du service.'
        )
        
        messages.success(request, f'Sortie d\'hospitalisation enregistrée pour {hospitalisation.patient.nom}.')
        return redirect('liste_hospitalisations')
    
    return render(request, 'consultations/sortie_hospitalisation.html', {
        'hospitalisation': hospitalisation
    })

@login_required
def historique_hospitalisation(request, hospitalisation_id):
    hospitalisation = get_object_or_404(Hospitalisation, id=hospitalisation_id)
    historiques = hospitalisation.historiques.order_by('-date_action')
    return render(request, 'consultations/historique_hospitalisation.html', {
        'hospitalisation': hospitalisation,
        'historiques': historiques
    })

@login_required
def export_historique_hospitalisation_pdf(request, hospitalisation_id):
    hospitalisation = get_object_or_404(Hospitalisation, id=hospitalisation_id)
    historiques = HistoriqueHospitalisation.objects.filter(hospitalisation=hospitalisation).order_by('-date_action')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historique_hospitalisation.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, 800, "Historique de l'hospitalisation")

    p.setFont("Helvetica", 12)
    y = 770
    p.drawString(50, y, f"Patient : {hospitalisation.patient.nom} {hospitalisation.patient.prenom}")
    y -= 20
    p.drawString(50, y, f"Service : {hospitalisation.service}")
    y -= 30

    for h in historiques:
        text = f"{localtime(h.date_action).strftime('%d/%m/%Y %H:%M')} | {h.utilisateur} | {h.action} | {h.details}"
        p.drawString(50, y, text)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response

@login_required
def prescrire_analyse(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        form = PrescriptionAnalyseForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.consultation = consultation
            prescription.prescripteur = request.user

            # Créer un type d’analyse s’il est absent
            if not prescription.type_analyse and prescription.autre_type_analyse:
                nouveau_type, created = TypeAnalyse.objects.get_or_create(nom=prescription.autre_type_analyse)
                prescription.type_analyse = nouveau_type

            prescription.save()

            messages.success(request, "🧪 Analyse prescrite avec succès.")
            return redirect('detail_consultation', consultation_id=consultation.id)
    else:
        form = PrescriptionAnalyseForm()

    return render(request, 'consultations/prescrire_analyse.html', {
        'form': form,
        'consultation': consultation
    })

def factures_ordonnances(request):
    factures = Facture.objects.filter(ordonnance__isnull=False).select_related('patient', 'ordonnance')
    return render(request, 'facturation/factures_par_ordonnance.html', {
        'factures': factures
    })

def factures_hospitalisations(request):
    factures = Facture.objects.filter(hospitalisation__isnull=False).select_related('patient', 'hospitalisation')
    return render(request, 'facturation/factures_par_hospitalisation.html', {
        'factures': factures
    })
