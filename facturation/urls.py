from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_factures, name='liste_factures'),
    path('ajouter/', views.ajouter_facture, name='ajouter_facture'),
    path('paiement/', views.enregistrer_paiement, name='ajouter_paiement'),
    path('facture/<int:facture_id>/', views.detail_facture, name='detail_facture'),
    path('facture/<int:facture_id>/pdf/', views.export_facture_pdf, name='export_facture_pdf'),
    path('export/pdf/', views.export_factures_pdf, name='export_factures_pdf'),
    path('export/excel/', views.export_factures_excel, name='export_factures_excel'),
    path('facture/<int:facture_id>/pdf/', views.export_facture_individuelle_pdf, name='export_facture_pdf'),
    path('remboursement/ajouter/', views.enregistrer_remboursement, name='ajouter_remboursement'),
    path('tableau-bord/', views.tableau_bord_facturation, name='tableau_bord_facturation'),
    path('export-tableau-bord-pdf/', views.export_tableau_bord_pdf, name='export_tableau_bord_pdf'),
    path('export-tableau-bord-excel/', views.export_tableau_bord_excel, name='export_tableau_bord_excel'),


]