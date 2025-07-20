from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Soin, HistoriqueSoin
from .forms import SoinForm, HistoriqueSoinFilterForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from django.http import HttpResponse

# Liste des soins
@login_required
def liste_soins(request):
    soins = Soin.objects.select_related('patient', 'personnel').order_by('-date_soin')
    return render(request, 'soins/liste_soins.html', {'soins': soins})

# Ajouter un soin
@login_required
def ajouter_soin(request):
    if request.method == 'POST':
        form = SoinForm(request.POST)
        if form.is_valid():
            soin = form.save(commit=False)
            soin.utilisateur = request.user
            soin.save()

            HistoriqueSoin.objects.create(
                soin=soin,
                utilisateur=request.user,
                action="ajout",
                details=f"Soin {soin.get_type_soin_display()} ajouté pour {soin.patient}"
            )

            messages.success(request, "Soin enregistré avec succès.")
            return redirect('soins:liste_soins')
    else:
        form = SoinForm()
    return render(request, 'soins/ajouter_soin.html', {'form': form})

# Modifier un soin
@login_required
def modifier_soin(request, soin_id):
    soin = get_object_or_404(Soin, id=soin_id)
    if request.method == 'POST':
        form = SoinForm(request.POST, instance=soin)
        if form.is_valid():
            form.save()

            HistoriqueSoin.objects.create(
                soin=soin,
                utilisateur=request.user,
                action="modification",
                details=f"Soin modifié pour {soin.patient}"
            )

            messages.success(request, "Soin modifié avec succès.")
            return redirect('soins:liste_soins')
    else:
        form = SoinForm(instance=soin)
    return render(request, 'soins/modifier_soin.html', {'form': form, 'soin': soin})

# Supprimer un soin
@login_required
def supprimer_soin(request, soin_id):
    soin = get_object_or_404(Soin, id=soin_id)
    if request.method == 'POST':
        HistoriqueSoin.objects.create(
            soin=soin,
            utilisateur=request.user,
            action="suppression",
            details=f"Soin supprimé pour {soin.patient}"
        )
        soin.delete()
        messages.success(request, "Soin supprimé avec succès.")
        return redirect('soins:liste_soins')
    return render(request, 'soins/supprimer_soin.html', {'soin': soin})

# Historique des soins
@login_required
def historique_soins(request):
    soins = HistoriqueSoin.objects.select_related('soin__patient', 'utilisateur').all()
    form = HistoriqueSoinFilterForm(request.GET or None)

    if form.is_valid():
        patient_nom = form.cleaned_data.get('patient')
        type_soin = form.cleaned_data.get('type_soin')
        action = form.cleaned_data.get('action')
        utilisateur = form.cleaned_data.get('utilisateur')
        date_debut = form.cleaned_data.get('date_debut')
        date_fin = form.cleaned_data.get('date_fin')

        if patient_nom:
            soins = soins.filter(soin__patient__nom__icontains=patient_nom)
        if type_soin:
            soins = soins.filter(soin__type_soin=type_soin)
        if action:
            soins = soins.filter(action=action)
        if utilisateur:
            soins = soins.filter(utilisateur=utilisateur)
        if date_debut:
            soins = soins.filter(date_action__date__gte=date_debut)
        if date_fin:
            soins = soins.filter(date_action__date__lte=date_fin)

    soins = soins.order_by('-date_action')

    context = {
        'soins': soins,
        'form': form,
    }
    return render(request, 'soins/historique_soin.html', context)


@login_required
def export_soins_pdf(request):
    soins = Soin.objects.select_related('patient', 'utilisateur').order_by('-date_soin')
    template = get_template('soins/historique_soin_pdf.html')
    html = template.render({'soins': soins})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historique_soins.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response

@login_required
def export_soins_excel(request):
    soins = HistoriqueSoin.objects.select_related('soin', 'utilisateur').order_by('-date_action')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historique des soins"

    # Entêtes
    ws.append(["ID", "Patient", "Type de soin", "Date du soin", "Action", "Utilisateur", "Date de l'action"])

    for historique in soins:
        ws.append([
            historique.id,
            historique.soin.patient.nom_complet(),
            historique.soin.type_soin,
            historique.soin.date_soin.strftime('%Y-%m-%d %H:%M'),
            historique.action,
            historique.utilisateur.username,
            historique.date_action.strftime('%Y-%m-%d %H:%M'),
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=historique_soins.xlsx'
    wb.save(response)
    return response

@login_required
def export_historique_soin_pdf(request, soin_id):
    soin = get_object_or_404(Soin, id=soin_id)
    historiques = HistoriqueSoin.objects.filter(soin=soin).order_by('-date_action')

    template = get_template('soins/historique_soin_pdf.html')  # Tu dois créer ce fichier HTML si ce n’est pas encore fait
    html = template.render({'soin': soin, 'historiques': historiques})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historique_soin_{soin.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response

import openpyxl

@login_required
def export_historique_soin_excel(request, soin_id):
    soin = get_object_or_404(Soin, id=soin_id)
    historiques = HistoriqueSoin.objects.filter(soin=soin).order_by('-date_action')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Historique Soin {soin.id}"

    # En-têtes
    ws.append(["Date", "Action", "Utilisateur", "Détails"])

    for h in historiques:
        ws.append([
            h.date_action.strftime('%Y-%m-%d %H:%M'),
            h.get_action_display(),
            h.utilisateur.username,
            h.details
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="historique_soin_{soin.id}.xlsx"'
    wb.save(response)
    return response

from facturation.models import Facture
from django.shortcuts import render

def factures_soins(request):
    factures = Facture.objects.filter(soin__isnull=False).select_related('patient', 'soin')
    return render(request, 'facturation/factures_par_soin.html', {
        'factures': factures
    })

