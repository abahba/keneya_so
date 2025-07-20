from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    signup,
    redirection_tableau_de_bord,
    dashboard_medecin,
    dashboard_infirmier,
    dashboard_pharmacien,
    dashboard_imagerie,
    dashboard_laborantin,
    dashboard_admin,
    dashboard_assurance,
    dashboard_caissier,
    dashboard_secretariat
)

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    path('dashboard/medecin/', views.dashboard_medecin, name='dashboard_medecin'),
    path('dashboard/infirmier/', views.dashboard_infirmier, name='dashboard_infirmier'),
    path('dashboard/pharmacien/', views.dashboard_pharmacien, name='dashboard_pharmacien'),
    path('dashboard/imagerie/', views.dashboard_imagerie, name='dashboard_imagerie'),
    path('dashboard/laborantin/', views.dashboard_laborantin, name='dashboard_laborantin'),

    # Si besoin :
    path('dashboard/', views.redirection_tableau_de_bord, name='dashboard'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/redirect/', views.redirection_tableau_de_bord, name='redirection_tableau_de_bord'),
    path('rendezvous/', views.liste_rendezvous, name='liste_rendezvous'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
    path('dashboard/secretariat/', dashboard_secretariat, name='dashboard_secretariat'),
    path('dashboard/assurance/', dashboard_assurance, name='dashboard_assurance'),
    path('dashboard/caissier/', dashboard_caissier, name='dashboard_caissier'),
    path('dashboard/chirurgien/', views.dashboard_chirurgien, name='dashboard_chirurgien'),

]





