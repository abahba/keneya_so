from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, FileResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook
import io
from .models import PassageUrgence, HistoriqueUrgence
from .forms import PassageUrgenceForm, HistoriqueUrgenceFilterForm, UrgenceFilterForm
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def liste_urgences(request):
    urgences = PassageUrgence.objects.select_related('patient', 'utilisateur').order_by('-date_arrivee')
    form = UrgenceFilterForm(request.GET or None)

    if form.is_valid():
        type_urgence = form.cleaned_data.get('type_urgence')
        utilisateur = form.cleaned_data.get('utilisateur')
        date_debut = form.cleaned_data.get('date_debut')
        date_fin = form.cleaned_data.get('date_fin')

        if type_urgence:
            urgences = urgences.filter(type_urgence__icontains=type_urgence)
        if utilisateur:
            urgences = urgences.filter(utilisateur__username__icontains=utilisateur)
        if date_debut:
            urgences = urgences.filter(date_enregistrement__date__gte=date_debut)
        if date_fin:
            urgences = urgences.filter(date_enregistrement__date__lte=date_fin)

    return render(request, 'urgences/liste_urgences.html', {
        'urgences': urgences,
        'form': form
    })


@login_required
def ajouter_urgence(request):
    """Ajoute un nouveau passage aux urgences"""
    if request.method == 'POST':
        form = PassageUrgenceForm(request.POST)
        if form.is_valid():
            urgence = form.save(commit=False)
            urgence.utilisateur = request.user
            urgence.save()

            HistoriqueUrgence.objects.create(
                urgence=urgence,
                utilisateur=request.user,
                action="ajout",
                details=f"Ajout du passage aux urgences pour {urgence.patient}"
            )

            messages.success(request, "Passage aux urgences enregistré avec succès.")
            return redirect('urgences:liste_urgences')
    else:
        form = PassageUrgenceForm()

    return render(request, 'urgences/ajouter_urgence.html', {'form': form})

@login_required
def modifier_urgence(request, urgence_id):
    """Modifie un passage aux urgences existant"""
    urgence = get_object_or_404(PassageUrgence, id=urgence_id)

    if request.method == 'POST':
        form = PassageUrgenceForm(request.POST, instance=urgence)
        if form.is_valid():
            urgence = form.save()

            HistoriqueUrgence.objects.create(
                urgence=urgence,
                utilisateur=request.user,
                action="modification",
                details=f"Modification du passage aux urgences pour {urgence.patient}"
            )

            messages.success(request, "Passage aux urgences modifié avec succès.")
            return redirect('urgences:liste_urgences')
    else:
        form = PassageUrgenceForm(instance=urgence)

    return render(request, 'urgences/modifier_urgence.html', {
        'form': form, 
        'urgence': urgence
    })

@login_required
def supprimer_urgence(request, urgence_id):
    """Supprime un passage aux urgences"""
    urgence = get_object_or_404(PassageUrgence, id=urgence_id)

    if request.method == 'POST':
        HistoriqueUrgence.objects.create(
            urgence=urgence,
            utilisateur=request.user,
            action="suppression",
            details=f"Suppression du passage aux urgences pour {urgence.patient}"
        )
        urgence.delete()
        messages.success(request, "Passage aux urgences supprimé avec succès.")
        return redirect('urgences:liste_urgences')

    return render(request, 'urgences/supprimer_urgence.html', {'urgence': urgence})

@login_required
def historique_urgence(request, urgence_id):
    """Affiche l'historique des modifications d'un passage aux urgences"""
    urgence = get_object_or_404(PassageUrgence, id=urgence_id)
    historiques = HistoriqueUrgence.objects.filter(urgence=urgence).order_by('-date_action')

    form = HistoriqueUrgenceFilterForm(request.GET or None)
    if form.is_valid():
        if form.cleaned_data['action']:
            historiques = historiques.filter(action=form.cleaned_data['action'])
        if form.cleaned_data['utilisateur']:
            historiques = historiques.filter(utilisateur=form.cleaned_data['utilisateur'])
        if form.cleaned_data['date_debut']:
            historiques = historiques.filter(date_action__date__gte=form.cleaned_data['date_debut'])
        if form.cleaned_data['date_fin']:
            historiques = historiques.filter(date_action__date__lte=form.cleaned_data['date_fin'])

    return render(request, 'urgences/historique_urgence.html', {
        'urgence': urgence,
        'historiques': historiques,
        'form': form
    })

@login_required
def export_urgences_pdf(request):
    """Exporte la liste des urgences en PDF"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    # Configuration du document
    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "Liste des passages aux urgences")
    p.setFont("Helvetica", 12)
    
    # En-têtes du tableau
    headers = ["Patient", "Date arrivée", "Médecin", "Gravité", "État"]
    positions = [50, 150, 250, 350, 450]
    
    for i, header in enumerate(headers):
        p.drawString(positions[i], 770, header)
    
    # Ligne de séparation
    p.line(50, 765, 550, 765)
    
    y = 740
    urgences = PassageUrgence.objects.select_related(
        'patient', 'medecin_responsable'
    ).order_by('-date_passage')

    for urgence in urgences:
        if y < 100:  # Nouvelle page si nécessaire
            p.showPage()
            y = 800
            # Réécrire les en-têtes
            p.setFont("Helvetica-Bold", 16)
            p.drawString(180, 800, "Liste des urgences (suite)")
            p.setFont("Helvetica", 12)
            for i, header in enumerate(headers):
                p.drawString(positions[i], 770, header)
            p.line(50, 765, 550, 765)
            y = 740
        
        # Données
        p.drawString(50, y, str(urgence.patient))
        p.drawString(150, y, urgence.date_passage.strftime('%d/%m/%Y %H:%M'))
        p.drawString(250, y, str(urgence.medecin_responsable) if urgence.medecin_responsable else 'N/A')
        p.drawString(350, y, urgence.get_niveau_gravite_display() if hasattr(urgence, 'get_niveau_gravite_display') else '')
        p.drawString(450, y, urgence.etat_patient)
        
        y -= 20

    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="passages_urgences.pdf")

@login_required
def export_urgences_excel(request):
    """Exporte la liste des urgences en Excel"""
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=passages_urgences.xlsx'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Urgences"

    # En-têtes avec style
    headers = [
        "Patient", 
        "Date arrivée", 
        "Médecin responsable",
        "Niveau de gravité", 
        "État du patient", 
        "Observations"
    ]
    ws.append(headers)

    # Données
    urgences = PassageUrgence.objects.select_related(
        'patient', 'medecin_responsable'
    ).order_by('-date_passage')

    for urgence in urgences:
        ws.append([
            str(urgence.patient),
            urgence.date_passage.strftime('%d/%m/%Y %H:%M'),
            str(urgence.medecin_responsable) if urgence.medecin_responsable else '',
            urgence.get_niveau_gravite_display() if hasattr(urgence, 'get_niveau_gravite_display') else '',
            urgence.etat_patient,
            urgence.observations[:100] + '...' if urgence.observations and len(urgence.observations) > 100 else urgence.observations or ''
        ])

    # Ajuster la largeur des colonnes
    for col in ws.columns:
        max_length = max(
            (len(str(cell.value)) if cell.value else 0 
            for cell in col
        ))
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[col[0].column_letter].width = adjusted_width
        
    wb.save(response)
    return response
    
@login_required
def export_historique_urgence_pdf(request, urgence_id):
    """Exporte l'historique d'une urgence en PDF"""
    urgence = get_object_or_404(PassageUrgence, id=urgence_id)
    historiques = HistoriqueUrgence.objects.filter(urgence=urgence).order_by('-date_action')

    template_path = 'urgences/historique_urgence_pdf.html'
    context = {
        'urgence': urgence,
        'historiques': historiques,
        'date_export': timezone.now()
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historique_urgence_{urgence.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erreur lors de la génération du PDF", status=500)
    return response

@login_required
def export_historique_urgence_excel(request, urgence_id):
    """Exporte l'historique d'une urgence en Excel"""
    urgence = get_object_or_404(PassageUrgence, id=urgence_id)
    historiques = HistoriqueUrgence.objects.filter(urgence=urgence).order_by('-date_action')

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=historique_urgence_{urgence.id}.xlsx'

    wb = Workbook()
    ws = wb.active
    ws.title = f"Historique urgence"

    # En-têtes
    headers = ["Action", "Utilisateur", "Détails", "Date"]
    ws.append(headers)

    # Lignes de données
    for h in historiques:
        ws.append([
            h.get_action_display(),
            str(h.utilisateur),
            h.details,
            h.date_action.strftime("%d/%m/%Y %H:%M"),
        ])

    # Ajustement automatique de largeur
    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = max_length + 5

    wb.save(response)
    return response

from django.shortcuts import render
from facturation.models import Facture

def factures_urgences(request):
    factures = Facture.objects.filter(urgence__isnull=False).select_related('patient', 'urgence')
    return render(request, 'facturation/factures_par_urgences.html', {
        'factures': factures
    })

