from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils.timezone import now
from django.db.models.functions import TruncDate

from patients.models import Patient
from facturation.models import Facture, Paiement
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.db.models import Sum, Q

from consultations.models import Consultation, Ordonnance, Hospitalisation
from pharmacie.models import Medicament
from soins.models import Soin
from laboratoire.models import AnalyseBiologique
from imagerie.models import ExamenImagerie as Imagerie
from bloc_operatoire.models import OperationChirurgicale
from personnel.models import PersonnelMedical
from django.utils import timezone
today = timezone.now()


@login_required
def tableau_de_bord(request):
    today = now().date()

    # 📊 Statistiques principales
    stats = [
        ("Patients", Patient.objects.count()),
        ("Consultations", Consultation.objects.count()),
        ("Consultations aujourd'hui", Consultation.objects.filter(date_consultation=today).count()),
        ("Ordonnances", Ordonnance.objects.count()),
        ("Hospitalisations", Hospitalisation.objects.count()),
        ("Soins", Soin.objects.count()),
        ("Analyses", AnalyseBiologique.objects.count()),
        ("Imageries", Imagerie.objects.count()),
        ("Interventions", OperationChirurgicale.objects.count()),
        ("Personnel médical", PersonnelMedical.objects.count()),
        ("Médicaments", Medicament.objects.count()),
        ("Factures", Facture.objects.count()),
    ]

    # 💰 Statistiques financières
    revenus = Paiement.objects.aggregate(total=Sum('montant_verse'))['total'] or 0
    stats_financieres = [
        ("Factures payées", Facture.objects.filter(statut='payée').count()),
        ("Factures impayées", Facture.objects.filter(Q(statut='non_payée') | Q(statut='partielle')).count()),
        ("Revenus totaux (FCFA)", revenus),
    ]

    # 📈 Données pour les graphiques mensuels
    chart_data = {
        'consultations': Consultation.objects.filter(date_consultation__month=today.month).count(),
        'hospitalisations': Hospitalisation.objects.filter(date_entree__month=today.month).count(),
        'ordonnances': Ordonnance.objects.filter(date_creation__month=today.month).count(),
        'soins': Soin.objects.filter(date_soin__month=today.month).count(),
    }

    # 📅 Données hebdomadaires pour graphique
    consultations_par_jour = (
        Consultation.objects
        .filter(date_consultation__week=today.isocalendar()[1])  # semaine actuelle
        .annotate(jour=TruncDate('date_consultation'))
        .values('jour')
        .annotate(nombre=Count('id'))
        .order_by('jour')
    )

    jours_labels = [item['jour'].strftime('%A') for item in consultations_par_jour]
    jours_valeurs = [item['nombre'] for item in consultations_par_jour]

    # 🧠 Contexte global
    context = {
        'today': today,
        'stats': stats,
        'stats_financieres': stats_financieres,
        'chart_data': chart_data,
        'factures_payees': Facture.objects.filter(statut='payée').count(),
        'factures_non_payees': Facture.objects.filter(Q(statut='non_payée') | Q(statut='partielle')).count(),
        'jours_labels': jours_labels,
        'jours_valeurs': jours_valeurs,
    }

    return render(request, 'dashboard/tableau_de_bord.html', context)


@login_required
def export_dashboard_pdf(request):
    today = now().date()

    # 💰 Revenus
    revenus = Paiement.objects.aggregate(total=Sum('montant_verse'))['total'] or 0

    # 📊 Statistiques principales
    stats = [
        ("Patients", Patient.objects.count()),
        ("Consultations", Consultation.objects.count()),
        ("Consultations aujourd'hui", Consultation.objects.filter(date_consultation=today).count()),
        ("Ordonnances", Ordonnance.objects.count()),
        ("Hospitalisations", Hospitalisation.objects.count()),
        ("Soins", Soin.objects.count()),
        ("Analyses biologiques", AnalyseBiologique.objects.count()),
        ("Imageries", Imagerie.objects.count()),
        ("Interventions", OperationChirurgicale.objects.count()),
        ("Personnel médical", PersonnelMedical.objects.count()),
        ("Médicaments", Medicament.objects.count()),
        ("Factures", Facture.objects.count()),
    ]

    # 💸 Statistiques financières
    stats_financieres = [
        ("Factures payées", Facture.objects.filter(statut='payée').count()),
        ("Factures impayées", Facture.objects.filter(Q(statut='non_payée') | Q(statut='partielle')).count()),
        ("Revenus totaux (FCFA)", revenus),
    ]

    # 📄 Génération PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, y, "Tableau de Bord Global")
    y -= 40

    p.setFont("Helvetica-Bold", 13)
    p.drawString(50, y, f"Mise à jour : {today.strftime('%d/%m/%Y')}")
    y -= 30

    # Section Statistiques générales
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Statistiques Générales")
    y -= 20

    p.setFont("Helvetica", 11)
    for label, value in stats:
        p.drawString(60, y, f"{label} : {value}")
        y -= 18

    y -= 10
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Statistiques Financières")
    y -= 20

    p.setFont("Helvetica", 11)
    for label, value in stats_financieres:
        p.drawString(60, y, f"{label} : {value}")
        y -= 18

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="dashboard_global.pdf"'}
    )

from django.shortcuts import render, redirect
from .models import ParametresSysteme
from .forms import ParametresSystemeForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Optionnel : vérifier si l'utilisateur est super admin
def is_super_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_super_admin)
def parametres_systeme(request):
    parametres = ParametresSysteme.objects.first()
    
    if request.method == 'POST':
        form = ParametresSystemeForm(request.POST, request.FILES, instance=parametres)
        if form.is_valid():
            form.save()
            return redirect('parametres_systeme')
    else:
        form = ParametresSystemeForm(instance=parametres)

    return render(request, 'dashboard/parametres_systeme.html', {'form': form})


from accounts.models import CustomUser
from django.contrib import messages

@login_required
@user_passes_test(is_super_admin)
def gestion_utilisateurs(request):
    utilisateurs = CustomUser.objects.all()
    return render(request, 'dashboard/gestion_utilisateurs.html', {'utilisateurs': utilisateurs})

from django.contrib.auth import update_session_auth_hash

@login_required
@user_passes_test(is_super_admin)
def changer_statut_utilisateur(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()

    statut = "activé" if user.is_active else "désactivé"

    send_mail(
        'Changement de statut de votre compte',
        f'Bonjour {user.username},\n\nVotre compte a été {statut} par un administrateur.',
        'admin@keneyaso.com',
        [user.email],
        fail_silently=False,
    )

    messages.success(request, f"Statut de l'utilisateur mis à jour et email envoyé.")
    return redirect('gestion_utilisateurs')

@login_required
@user_passes_test(is_super_admin)
def modifier_role_utilisateur(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        role = request.POST.get('role')
        user.role = role
        user.save()
        messages.success(request, "Rôle mis à jour.")
        return redirect('gestion_utilisateurs')
    return render(request, 'dashboard/modifier_role.html', {'user': user})

from django.core.mail import send_mail

@login_required
@user_passes_test(is_super_admin)
def reinitialiser_mot_de_passe(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()
        send_mail(
            'Réinitialisation de votre mot de passe',
            f'Bonjour {user.username},\n\nVotre mot de passe a été réinitialisé par un administrateur. Veuillez vous connecter avec votre nouveau mot de passe.',
            'admin@keneyaso.com',
            [user.email],
            fail_silently=False,
        )
        messages.success(request, "Mot de passe réinitialisé et email envoyé.")
        return redirect('gestion_utilisateurs')
    return render(request, 'dashboard/reinitialiser_mot_de_passe.html', {'user': user})

