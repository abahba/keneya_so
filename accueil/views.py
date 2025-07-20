from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def redirection_tableau_de_bord(request):
    user = request.user
    if user.role == 'admin':
        return redirect('dashboard_admin')
    elif user.role == 'medecin':
        return redirect('dashboard_medecin')
    elif user.role == 'infirmier':
        return redirect('dashboard_infirmier')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'accueil/index.html')

