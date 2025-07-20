from django.urls import path
from . import views

app_name = 'bloc_operatoire'

urlpatterns = [
    # Opérations chirurgicales
    path('', views.liste_operations, name='liste_operations'),
    path('ajouter/', views.ajouter_operation, name='ajouter_operation'),
    path('modifier/<int:operation_id>/', views.modifier_operation, name='modifier_operation'),
    path('supprimer/<int:operation_id>/', views.supprimer_operation, name='supprimer_operation'),
    
    # Exports globaux
    path('export/pdf/', views.export_operations_pdf, name='export_operations_pdf'),
    path('export/excel/', views.export_operations_excel, name='export_operations_excel'),
    
    # Historique des opérations
    path('historique/<int:operation_id>/', views.historique_operation, name='historique_operation'),
    path('historique/<int:operation_id>/pdf/', views.export_historique_operation_pdf, name='export_historique_operation_pdf'),
    path('historique/<int:operation_id>/excel/', views.export_historique_operation_excel, name='export_historique_operation_excel'),
    path('factures/operations/', views.factures_operations, name='factures_operations'),
]
