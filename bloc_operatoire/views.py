from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
import xlsxwriter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from .models import OperationChirurgicale, HistoriqueOperation
from .forms import OperationChirurgicaleForm
from django.utils import timezone
from .forms import HistoriqueOperationFilterForm

@login_required
def liste_operations(request):
    """Affiche la liste des opérations chirurgicales"""
    operations = OperationChirurgicale.objects.select_related(
        'patient', 'chirurgien', 'anesthesiste', 'utilisateur'
    ).order_by('-date_operation')
    return render(request, 'bloc_operatoire/liste_operations.html', {
        'operations': operations
    })

@login_required
def ajouter_operation(request):
    """Ajoute une nouvelle opération chirurgicale"""
    if request.method == 'POST':
        form = OperationChirurgicaleForm(request.POST)
        if form.is_valid():
            operation = form.save(commit=False)
            operation.utilisateur = request.user
            operation.save()
            
            # Création de l'historique
            HistoriqueOperation.objects.create(
                operation=operation,
                utilisateur=request.user,
                action='ajout',
                details=f"Ajout de l'opération {operation.type_operation}"
            )
            
            messages.success(request, "L'opération a été ajoutée avec succès!")
            return redirect('liste_operations')
    else:
        initial = {}
        if hasattr(request.user, 'personnelmedical'):
            initial['chirurgien'] = request.user.personnelmedical
        form = OperationChirurgicaleForm(initial=initial)
    
    return render(request, 'bloc_operatoire/ajouter_operation.html', {'form': form})

@login_required
def modifier_operation(request, operation_id):
    """Modifie une opération existante"""
    operation = get_object_or_404(OperationChirurgicale, id=operation_id)
    
    if request.method == 'POST':
        form = OperationChirurgicaleForm(request.POST, instance=operation)
        if form.is_valid():
            operation = form.save()
            
            HistoriqueOperation.objects.create(
                operation=operation,
                utilisateur=request.user,
                action='modification',
                details=f"Modification de l'opération {operation.type_operation}"
            )
            
            messages.success(request, "L'opération a été modifiée avec succès!")
            return redirect('liste_operations')
    else:
        form = OperationChirurgicaleForm(instance=operation)
    
    return render(request, 'bloc_operatoire/modifier_operation.html', {
        'form': form,
        'operation': operation
    })

@login_required
def supprimer_operation(request, operation_id):
    """Supprime une opération après confirmation"""
    operation = get_object_or_404(OperationChirurgicale, id=operation_id)
    
    if request.method == 'POST':
        HistoriqueOperation.objects.create(
            operation=operation,
            utilisateur=request.user,
            action='suppression',
            details=f"Suppression de l'opération {operation.type_operation}"
        )
        
        operation.delete()
        messages.success(request, "L'opération a été supprimée avec succès!")
        return redirect('liste_operations')
    
    return render(request, 'bloc_operatoire/supprimer_operation.html', {
        'operation': operation
    })

@login_required
def historique_operation(request, pk):
    operation = get_object_or_404(OperationChirurgicale, pk=pk)
    historiques = HistoriqueOperation.objects.filter(operation=operation).order_by('-date_action')

    form = HistoriqueOperationFilterForm(request.GET or None)

    if form.is_valid():
        action = form.cleaned_data.get('action')
        utilisateur = form.cleaned_data.get('utilisateur')
        date_debut = form.cleaned_data.get('date_debut')
        date_fin = form.cleaned_data.get('date_fin')

        if action:
            historiques = historiques.filter(action__icontains=action)
        if utilisateur:
            historiques = historiques.filter(utilisateur__username__icontains=utilisateur)
        if date_debut:
            historiques = historiques.filter(date_action__date__gte=date_debut)
        if date_fin:
            historiques = historiques.filter(date_action__date__lte=date_fin)

    context = {
        'operation': operation,
        'historiques': historiques,
        'form': form
    }
    return render(request, 'bloc_operatoire/historique_operation.html', context)

@login_required
def export_operations_pdf(request):
    """Exporte la liste des opérations en PDF"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    # Configuration du document
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, "Liste des opérations chirurgicales")
    p.setFont("Helvetica", 12)
    
    # En-têtes du tableau
    p.drawString(50, 770, "Patient")
    p.drawString(200, 770, "Type d'opération")
    p.drawString(350, 770, "Date")
    p.drawString(450, 770, "Chirurgien")
    
    # Ligne de séparation
    p.line(50, 765, 550, 765)
    
    y = 740
    operations = OperationChirurgicale.objects.select_related(
        'patient', 'chirurgien'
    ).order_by('-date_operation')

    for op in operations:
        if y < 100:  # Nouvelle page si on arrive en bas
            p.showPage()
            y = 800
            # Réécrire les en-têtes
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, 800, "Liste des opérations chirurgicales (suite)")
            p.setFont("Helvetica", 12)
            p.drawString(50, 770, "Patient")
            p.drawString(200, 770, "Type d'opération")
            p.drawString(350, 770, "Date")
            p.drawString(450, 770, "Chirurgien")
            p.line(50, 765, 550, 765)
            y = 740
        
        p.drawString(50, y, op.patient.nom_complet)
        p.drawString(200, y, op.type_operation)
        p.drawString(350, y, op.date_operation.strftime('%d/%m/%Y'))
        p.drawString(450, y, op.chirurgien.nom_complet if op.chirurgien else 'N/A')
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="operations_chirurgicales.pdf")

@login_required
def export_operations_excel(request):
    """Exporte la liste des opérations en Excel"""
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=operations_chirurgicales.xlsx'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Opérations"

    # En-têtes avec style
    headers = ["Patient", "Type d'opération", "Date", "Chirurgien", "Anesthésiste", "Salle", "Compte rendu"]
    ws.append(headers)

    # Données
    operations = OperationChirurgicale.objects.select_related(
        'patient', 'chirurgien', 'anesthesiste'
    ).order_by('-date_operation')

    for op in operations:
        ws.append([
            op.patient.nom_complet,
            op.type_operation,
            op.date_operation.strftime('%d/%m/%Y %H:%M'),
            op.chirurgien.nom_complet if op.chirurgien else '',
            op.anesthesiste.nom_complet if op.anesthesiste else '',
            op.salle,
            op.compte_rendu[:100] + '...' if len(op.compte_rendu) > 100 else op.compte_rendu
        ])

    # Ajuster la largeur des colonnes
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

    wb.save(response)
    return response

@login_required
def export_historique_operation_pdf(request, operation_id):
    """Exporte l'historique d'une opération en PDF"""
    operation = get_object_or_404(OperationChirurgicale, id=operation_id)
    historiques = operation.historiques.all().order_by('-date_action')
    
    template_path = 'bloc_operatoire/historique_operation_pdf.html'
    context = {
        'operation': operation,
        'historiques': historiques,
        'date_export': timezone.now().strftime("%d/%m/%Y %H:%M")
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historique_operation_{operation.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response

@login_required
def export_historique_operation_excel(request, operation_id):
    """Exporte l'historique d'une opération en Excel"""
    operation = get_object_or_404(OperationChirurgicale, id=operation_id)
    historiques = operation.historiques.all().order_by('-date_action')

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(f'Historique Opération {operation.id}')

    # Formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm'})

    # En-têtes
    headers = ['Action', 'Utilisateur', 'Détails', 'Date']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    # Données
    for row_num, historique in enumerate(historiques, 1):
        worksheet.write(row_num, 0, historique.get_action_display())
        worksheet.write(row_num, 1, str(historique.utilisateur))
        worksheet.write(row_num, 2, historique.details)
        worksheet.write_datetime(row_num, 3, historique.date_action, date_format)

    # Ajuster la largeur des colonnes
    worksheet.set_column(0, 0, 15)  # Action
    worksheet.set_column(1, 1, 25)  # Utilisateur
    worksheet.set_column(2, 2, 50)  # Détails
    worksheet.set_column(3, 3, 20)  # Date

    workbook.close()
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="historique_operation_{operation.id}.xlsx"'
    return response

from facturation.models import Facture
from django.shortcuts import render

def factures_operations(request):
    factures = Facture.objects.filter(operation__isnull=False).select_related('patient', 'operation')
    return render(request, 'facturation/factures_par_operation.html', {
        'factures': factures
    })

