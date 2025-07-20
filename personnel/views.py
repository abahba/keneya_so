from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PersonnelMedical, HistoriquePersonnel
from .forms import PersonnelForm


# ➕ Ajouter un membre du personnel
@login_required
def ajouter_personnel(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            personnel = form.save()
            HistoriquePersonnel.objects.create(
                personnel=personnel,
                utilisateur=request.user,
                action='ajout',
                details='Ajout du personnel médical.'
            )
            return redirect('liste_personnel')
    else:
        form = PersonnelForm()
    return render(request, 'personnel/ajouter_personnel.html', {'form': form})


# 📋 Liste de tout le personnel actif
@login_required
def liste_personnel(request):
    personnels = PersonnelMedical.objects.filter(actif=True)
    return render(request, 'personnel/liste_personnel.html', {'personnels': personnels})


# ✏️ Modifier un personnel existant
@login_required
def modifier_personnel(request, pk):
    personnel = get_object_or_404(PersonnelMedical, pk=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, instance=personnel)
        if form.is_valid():
            form.save()
            HistoriquePersonnel.objects.create(
                personnel=personnel,
                utilisateur=request.user,
                action='modification',
                details='Modification des informations du personnel.'
            )
            return redirect('liste_personnel')
    else:
        form = PersonnelForm(instance=personnel)
    return render(request, 'personnel/modifier_personnel.html', {'form': form})


# 🗑️ Suppression (soft delete) d’un personnel
@login_required
def supprimer_personnel(request, pk):
    personnel = get_object_or_404(PersonnelMedical, pk=pk)
    if request.method == 'POST':
        personnel.actif = False
        personnel.save()
        HistoriquePersonnel.objects.create(
            personnel=personnel,
            utilisateur=request.user,
            action='suppression',
            details='Désactivation du personnel.'
        )
        return redirect('liste_personnel')
    return render(request, 'personnel/supprimer_personnel.html', {'personnel': personnel})


# 🕘 Historique des actions d’un personnel
@login_required
def historique_personnel(request, personnel_id):
    personnel = get_object_or_404(PersonnelMedical, id=personnel_id)
    historiques = personnel.historiques.order_by('-date_action')  # related_name="historiques"
    return render(request, 'personnel/historique_personnel.html', {
        'personnel': personnel,
        'historiques': historiques
    })

