from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Medicament
from .forms import MedicamentForm
from .models import Medicament, HistoriqueMedicament
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import openpyxl
from openpyxl.styles import Font

# ➕ Ajouter un médicament
@login_required
def ajouter_medicament(request):
    if request.method == 'POST':
        form = MedicamentForm(request.POST)
        if form.is_valid():
            medicament = form.save()
            HistoriqueMedicament.objects.create(
                medicament=medicament,
                utilisateur=request.user,
                action="ajout",
                details=f"Ajout du médicament {medicament.nom}."
            )
            return redirect('liste_medicaments')
    else:
        form = MedicamentForm()
    return render(request, 'pharmacie/ajouter_medicament.html', {'form': form})

# 📋 Liste des médicaments
@login_required
def liste_medicaments(request):
    medicaments = Medicament.objects.all()
    return render(request, 'pharmacie/liste_medicaments.html', {'medicaments': medicaments})

# ✏️ Modifier un médicament
@login_required
def modifier_medicament(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        form = MedicamentForm(request.POST, instance=medicament)
        if form.is_valid():
            form.save()
            HistoriqueMedicament.objects.create(
                medicament=medicament,
                utilisateur=request.user,
                action="modification",
                details=f"Médicament modifié : {medicament.nom}"
            )
            return redirect('liste_medicaments')
    else:
        form = MedicamentForm(instance=medicament)
    return render(request, 'pharmacie/modifier_medicament.html', {'form': form})

# ❌ Supprimer un médicament
@login_required
def supprimer_medicament(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        medicament.actif = False
        medicament.save()
        HistoriqueMedicament.objects.create(
            medicament=medicament,
            utilisateur=request.user,
            action="suppression",
            details=f"Médicament supprimé (désactivé) : {medicament.nom}"
        )
        return redirect('liste_medicaments')
    return render(request, 'pharmacie/supprimer_medicament.html', {'medicament': medicament})

@login_required
def historique_medicament(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    historiques = medicament.historiques.order_by('-date_action')
    return render(request, 'pharmacie/historique_medicament.html', {
        'medicament': medicament,
        'historiques': historiques
    })

@login_required
def export_historique_medicament_pdf(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    historiques = medicament.historiques.order_by('-date_action')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historique_{medicament.nom}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Historique - {medicament.nom}")
    y = 770
    p.setFont("Helvetica", 12)

    for h in historiques:
        ligne = f"{h.date_action.strftime('%d/%m/%Y %H:%M')} | {h.utilisateur} | {h.action} | {h.details}"
        p.drawString(30, y, ligne)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response


@login_required
def export_historique_medicament_excel(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    historiques = medicament.historiques.order_by('-date_action')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Historique - {medicament.nom}"

    headers = ['Date', 'Utilisateur', 'Action', 'Détails']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for h in historiques:
        ws.append([
            h.date_action.strftime('%d/%m/%Y %H:%M'),
            str(h.utilisateur),
            h.action,
            h.details
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"historique_{medicament.nom}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response

