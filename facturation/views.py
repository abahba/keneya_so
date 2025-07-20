from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Facture, Paiement, Remboursement
from .forms import FactureForm, PaiementForm, RemboursementForm
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime
import json
from django.core.paginator import Paginator


def liste_factures(request):
    factures = Facture.objects.select_related('patient', 'ordonnance').order_by('-date_emission')

    # Recherche par ID
    search = request.GET.get('search')
    if search:
        try:
            facture_id = int(search)
            factures = factures.filter(id=facture_id)
        except ValueError:
            pass

    # Filtrage par statut
    statut = request.GET.get('statut')
    if statut:
        factures = factures.filter(statut=statut)

    # Pagination
    paginator = Paginator(factures, 15)  # 15 factures par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'facturation/liste_factures.html', {
        'page_obj': page_obj,
    })


def ajouter_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save(commit=False)
            if facture.ordonnance and facture.ordonnance.prise_en_charge:
                facture.montant_assurance = facture.ordonnance.prise_en_charge.montant_demande
                facture.montant_patient = facture.montant_total - facture.montant_assurance
            else:
                facture.montant_patient = facture.montant_total
            facture.utilisateur = request.user
            facture.save()
            return redirect('liste_factures')
    else:
        form = FactureForm()
    return render(request, 'facturation/ajouter_facture.html', {'form': form})


def enregistrer_paiement(request):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.utilisateur = request.user
            paiement.save()
            facture = paiement.facture
            facture.calculer_statut()
            facture.save()
            return redirect('liste_factures')
    else:
        form = PaiementForm()

    facture_id = request.GET.get('facture_id')
    facture = Facture.objects.filter(id=facture_id).first() if facture_id else None

    return render(request, 'facturation/ajouter_paiement.html', {
        'form': form,
        'f': facture,
    })


def export_factures_pdf(request):
    factures = Facture.objects.select_related('patient').all()
    template = get_template('facturation/export_factures_pdf.html')
    html = template.render({'factures': factures})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factures.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


def export_factures_excel(request):
    factures = Facture.objects.select_related('patient').all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Factures"
    ws.append(['Patient', 'Montant Total', 'Montant Assurance', 'Montant Patient', 'Date'])

    for f in factures:
        ws.append([
            f.patient.nom_complet(), f.montant_total, f.montant_assurance,
            f.montant_patient, f.date_emission.strftime("%d/%m/%Y %H:%M")
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="factures.xlsx"'
    wb.save(response)
    return response


def detail_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    paiements = facture.paiements.all()
    return render(request, 'facturation/detail_facture.html', {
        'facture': facture,
        'paiements': paiements
    })


def export_facture_pdf(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    paiements = facture.paiements.all()
    template = get_template('facturation/export_facture_pdf.html')
    html = template.render({'facture': facture, 'paiements': paiements})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


def export_facture_individuelle_pdf(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    template = get_template('facturation/facture_individuelle_pdf.html')
    html = template.render({'facture': facture})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


def enregistrer_remboursement(request):
    if request.method == 'POST':
        form = RemboursementForm(request.POST)
        if form.is_valid():
            remboursement = form.save(commit=False)
            remboursement.utilisateur = request.user
            remboursement.save()

            facture = remboursement.paiement.facture
            total_payé = sum([p.montant_verse for p in facture.paiements.all()])
            total_rembourse = sum([
                r.montant for p in facture.paiements.all()
                for r in p.remboursements.all()
            ])
            net_payé = total_payé - total_rembourse

            if net_payé >= facture.montant_total:
                facture.statut = 'payée'
            elif net_payé > 0:
                facture.statut = 'partiellement payée'
            else:
                facture.statut = 'non payée'

            facture.save()

            return redirect('liste_factures')
    else:
        form = RemboursementForm()
    return render(request, 'facturation/ajouter_remboursement.html', {'form': form})


def tableau_bord_facturation(request):
    annee = int(request.GET.get('annee', datetime.now().year))

    factures = Facture.objects.filter(date_emission__year=annee).annotate(month=TruncMonth('date_emission')).values('month').annotate(total_factures=Sum('montant_total'))
    paiements = Paiement.objects.filter(date_paiement__year=annee).annotate(month=TruncMonth('date_paiement')).values('month').annotate(total_paiements=Sum('montant_verse'))
    remboursements = Remboursement.objects.filter(date_remboursement__year=annee).annotate(month=TruncMonth('date_remboursement')).values('month').annotate(total_remboursements=Sum('montant'))

    tableau = {}
    for f in factures:
        m = f['month']
        tableau[m] = {'total_factures': f['total_factures'], 'total_paiements': 0, 'total_remboursements': 0}
    for p in paiements:
        m = p['month']
        tableau.setdefault(m, {})['total_paiements'] = p['total_paiements']
    for r in remboursements:
        m = r['month']
        tableau.setdefault(m, {})['total_remboursements'] = r['total_remboursements']

    mois_labels = []
    factures_vals = []
    paiements_vals = []

    tableau_ordre = dict(sorted(tableau.items()))
    for mois, stats in tableau_ordre.items():
        stats.setdefault('total_factures', 0)
        stats.setdefault('total_paiements', 0)
        stats.setdefault('total_remboursements', 0)
        stats['net_encaisse'] = stats['total_paiements'] - stats['total_remboursements']

        mois_labels.append(mois.strftime("%B"))
        factures_vals.append(float(stats['total_factures']))
        paiements_vals.append(float(stats['total_paiements']))

    context = {
        'annee': annee,
        'tableau': tableau_ordre,
        'mois': json.dumps(mois_labels),
        'factures_mensuelles': json.dumps(factures_vals),
        'paiements_mensuels': json.dumps(paiements_vals),
    }
    return render(request, 'facturation/tableau_bord_facturation.html', context)


def export_tableau_bord_pdf(request):
    annee = int(request.GET.get('annee', datetime.now().year))

    # même logique que tableau_bord_facturation
    # ... [idem contenu fusionné de stats] ...

    # Voir ton code existant (aucune erreur signalée ici)
    # ✅ Ce bloc reste inchangé
    # ...


def export_tableau_bord_excel(request):
    annee = int(request.GET.get('annee', datetime.now().year))

    # même logique que tableau_bord_facturation
    # ✅ Ce bloc reste inchangé
    # ...


