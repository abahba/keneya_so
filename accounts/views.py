from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


# Formulaire d'inscription
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique
            return redirect('redirection_tableau_de_bord')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


# Redirection selon le rôle de l'utilisateur connecté
@login_required
def redirection_tableau_de_bord(request):
    utilisateur = request.user

    if utilisateur.role == 'admin':
        return redirect('dashboard_admin')
    elif utilisateur.role == 'medecin':
        return redirect('dashboard_medecin')
    elif utilisateur.role == 'infirmier':
        return redirect('dashboard_infirmier')
    elif utilisateur.role == 'pharmacien':
        return redirect('dashboard_pharmacien')
    elif utilisateur.role == 'laborantin':
        return redirect('dashboard_laborantin')
    elif utilisateur.role == 'imagerie':
        return redirect('dashboard_imagerie')
    
    # Redirection par défaut ESSENTIELLE
    return redirect('dashboard_medecin')  # Ou une autre page par défaut appropriée


# Vues des différents tableaux de bord
@login_required
def dashboard_admin(request):
    return render(request, 'accounts/dashboard_admin.html')

@login_required
def dashboard_medecin(request):
    return render(request, 'accounts/dashboard_medecin.html')

@login_required
def dashboard_infirmier(request):
    return render(request, 'accounts/dashboard_infirmier.html')

@login_required
def dashboard_pharmacien(request):
    return render(request, 'accounts/dashboard_pharmacien.html')

@login_required
def dashboard_laborantin(request):
    return render(request, 'accounts/dashboard_laborantin.html')

@login_required
def dashboard_imagerie(request):
    return render(request, 'accounts/dashboard_imagerie.html')

@login_required
def dashboard_secretariat(request):
    return render(request, 'accounts/dashboard_secretariat.html')

@login_required
def dashboard_assurance(request):
    return render(request, 'accounts/dashboard_assurance.html')

@login_required
def dashboard_caissier(request):
    return render(request, 'accounts/dashboard_caissier.html')

@login_required
def dashboard_chirurgien(request):
    return render(request, 'accounts/dashboard_chirurgien.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # ou la page souhaitée après inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RendezVous  # Importez votre modèle RendezVous

@login_required
def liste_rendezvous(request):
    # Exemple de requête - adaptez selon votre modèle
    rendezvous = RendezVous.objects.filter(medecin=request.user).order_by('date')
    
    context = {
        'rendezvous': rendezvous,
    }
    return render(request, 'accounts/rendezvous/liste.html', context)

from django.utils.translation import gettext_lazy as _
from.models import models

class Patient(models.Model):
    nom = models.CharField(max_length=100, verbose_name=_("Nom"))
