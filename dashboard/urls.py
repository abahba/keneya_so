from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.tableau_de_bord, name='tableau_de_bord'),
    path('export_dashboard/pdf/', views.export_dashboard_pdf, name='export_dashboard_pdf'),
    path('parametres/', views.parametres_systeme, name='parametres_systeme'),
    path('utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('utilisateur/<int:user_id>/changer-statut/', views.changer_statut_utilisateur, name='changer_statut_utilisateur'),
    path('utilisateur/<int:user_id>/modifier-role/', views.modifier_role_utilisateur, name='modifier_role_utilisateur'),
    path('utilisateur/<int:user_id>/reinitialiser-mdp/', views.reinitialiser_mot_de_passe, name='reinitialiser_mot_de_passe'),


]
