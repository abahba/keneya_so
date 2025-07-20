from django.urls import path
from . import views
from .views import historique_consultation
from .views import export_historique_consultation_pdf, export_historique_consultation_excel

urlpatterns = [
    path('', views.liste_consultations, name='liste_consultations'),
    path('ajouter/', views.ajouter_consultation, name='ajouter_consultation'),
    path('modifier/<int:pk>/', views.modifier_consultation, name='modifier_consultation'),
    path('supprimer/<int:pk>/', views.supprimer_consultation, name='supprimer_consultation'),

    path('consultations/<int:consultation_id>/historique/', historique_consultation, name='historique_consultation'),
    path('consultations/<int:consultation_id>/historique/pdf/', export_historique_consultation_pdf, name='export_historique_consultation_pdf'),
    path('consultations/<int:consultation_id>/historique/excel/', export_historique_consultation_excel, name='export_historique_consultation_excel'),
    
    path('dossier/<int:patient_id>/', views.voir_dossier_medical, name='voir_dossier_medical'),
    path('dossier/creer/<int:patient_id>/', views.creer_dossier_medical, name='creer_dossier_medical'),
    path('dossier/modifier/<int:patient_id>/', views.modifier_dossier_medical, name='modifier_dossier_medical'),

    path('consultation/<int:consultation_id>/ordonnance/ajouter/', views.creer_ordonnance, name='creer_ordonnance'),
    path('ordonnance/<int:ordonnance_id>/', views.voir_ordonnance, name='voir_ordonnance'),

    path('ordonnance/creer/<int:consultation_id>/', views.creer_ordonnance, name='creer_ordonnance'),
    path('ordonnance/<int:ordonnance_id>/', views.voir_ordonnance, name='voir_ordonnance'),
    path('ordonnance/<int:ordonnance_id>/pdf/', views.export_ordonnance_pdf, name='export_ordonnance_pdf'),
    path('ordonnance/<int:ordonnance_id>/signer/', views.signer_ordonnance, name='signer_ordonnance'),

    path('hospitalisations/', views.liste_hospitalisations, name='liste_hospitalisations'),
    path('hospitalisations/ajouter/', views.ajouter_hospitalisation, name='ajouter_hospitalisation'),
    path('hospitalisations/modifier/<int:hospitalisation_id>/', views.modifier_hospitalisation, name='modifier_hospitalisation'),
    path('hospitalisations/sortie/<int:pk>/', views.marquer_sortie_hospitalisation, name='sortie_hospitalisation'),
    path('hospitalisations/historique/<int:hospitalisation_id>/', views.historique_hospitalisation, name='historique_hospitalisation'),
    path('hospitalisations/historique/<int:hospitalisation_id>/pdf/', views.export_historique_hospitalisation_pdf, name='export_historique_hospitalisation_pdf'),
    path('consultation/<int:consultation_id>/prescrire-analyse/', views.prescrire_analyse, name='prescrire_analyse'),

    path('factures/ordonnances/', views.factures_ordonnances, name='factures_ordonnances'),
    path('factures/hospitalisations/', views.factures_hospitalisations, name='factures_hospitalisations'),
]

