from django.urls import path
from . import views

app_name = 'soins'

urlpatterns = [
    path('', views.liste_soins, name='liste_soins'),
    path('ajouter/', views.ajouter_soin, name='ajouter_soin'),
    path('modifier/<int:soin_id>/', views.modifier_soin, name='modifier_soin'),
    path('supprimer/<int:soin_id>/', views.supprimer_soin, name='supprimer_soin'),
    path('historique/', views.historique_soins, name='historique_soins'),


    # Exports
    path('export/pdf/', views.export_soins_pdf, name='export_soins_pdf'),
    path('export/excel/', views.export_soins_excel, name='export_soins_excel'),
    path('export/historique/<int:soin_id>/pdf/', views.export_historique_soin_pdf, name='export_historique_soin_pdf'),
    path('export/historique/<int:soin_id>/excel/', views.export_historique_soin_excel, name='export_historique_soin_excel'),
    path('factures/soins/', views.factures_soins, name='factures_soins'),

]
