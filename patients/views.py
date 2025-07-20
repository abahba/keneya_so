from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PatientForm
from .models import Patient, HistoriquePatient
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils.timezone import localtime
import openpyxl
from django.http import HttpResponse

# Ajouter un patient
@login_required
def ajouter_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, user=request.user)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.modifie_par = request.user
            patient.save()
            HistoriquePatient.objects.create(
                patient=patient,
                action='création',
                utilisateur=request.user,
                details='Patient ajouté.'
            )
            return redirect('liste_patients')
    else:
        form = PatientForm(user=request.user)
    return render(request, 'patients/ajouter_patient.html', {'form': form})


# Liste des patients
@login_required
def liste_patients(request):
    statut = request.GET.get('statut')
    if statut:
        patients = Patient.objects.filter(actif=True, statut=statut)
    else:
        patients = Patient.objects.filter(actif=True)
    return render(request, 'patients/liste_patients.html', {'patients': patients})


# Modifier un patient
@login_required
def modifier_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient, user=request.user)
        if form.is_valid():
            form.instance.modifie_par = request.user
            form.save()
            HistoriquePatient.objects.create(
                patient=patient,
                action='modification',
                utilisateur=request.user,
                details=f'Modification du patient. Nouveau statut : {form.instance.statut}'
            )
            return redirect('liste_patients')
    else:
        form = PatientForm(instance=patient, user=request.user)

    return render(request, 'patients/modifier_patient.html', {'form': form, 'patient': patient})


# Suppression (désactivation) d’un patient
@login_required
def supprimer_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        patient.actif = False
        patient.save()
        HistoriquePatient.objects.create(
            patient=patient,
            action='suppression',
            utilisateur=request.user,
            details='Patient désactivé (soft delete).'
        )
        return redirect('liste_patients')

    return render(request, 'patients/supprimer_patient.html', {'patient': patient})


# Historique des actions d’un patient
@login_required
def historique_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    historiques = patient.historiques.all()

    # Filtrage par action
    action = request.GET.get('action')
    if action:
        historiques = historiques.filter(action=action)

    # Filtrage par date (format YYYY-MM-DD)
    date = request.GET.get('date')
    if date:
        historiques = historiques.filter(date_action__date=date)

    historiques = historiques.order_by('-date_action')

    return render(request, 'patients/historique_patient.html', {
        'patient': patient,
        'historiques': historiques
    })
@login_required
def export_pdf_historique(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    logs = patient.historiques.order_by('-date_action')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historique_{patient.nom}_{patient.prenom}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, f"Historique du patient : {patient.nom} {patient.prenom}")

    y = 770
    p.setFont("Helvetica", 10)
    for log in logs:
        date_str = localtime(log.date_action).strftime("%d/%m/%Y %H:%M")
        line = f"{date_str} | {log.action} | {log.utilisateur} | {log.details}"
        p.drawString(50, y, line)
        y -= 20
        if y < 40:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response
@login_required
def export_excel_historique(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    logs = patient.historiques.order_by('-date_action')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historique"

    ws.append(['Date', 'Action', 'Utilisateur', 'Détails'])

    for log in logs:
        date_str = localtime(log.date_action).strftime("%d/%m/%Y %H:%M")
        ws.append([date_str, log.action, str(log.utilisateur), log.details])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"historique_{patient.nom}_{patient.prenom}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response


