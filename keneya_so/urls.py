from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from accounts.views import redirection_tableau_de_bord

urlpatterns = i18n_patterns(
    path('', redirection_tableau_de_bord, name='redirection'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('patients/', include('patients.urls')),
    path('personnel/', include('personnel.urls')),
    path('pharmacie/', include('pharmacie.urls')),
    path('consultations/', include('consultations.urls')),
    path('assurances/', include('assurances.urls')),
    path('factures/', include('facturation.urls')),
    path('laboratoire/', include('laboratoire.urls')),
    path('imagerie/', include('imagerie.urls')),
    path('bloc-operatoire/', include('bloc_operatoire.urls')),
    path('urgences/', include(('urgences.urls', 'urgences'), namespace='urgences')),
    path('soins/', include(('soins.urls', 'soins'), namespace='soins')),
    path('administration/', include(('administration.urls', 'administration'), namespace='administration')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('accueil/', include('accueil.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]



