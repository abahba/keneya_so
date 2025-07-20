from django.apps import AppConfig


class BlocOperatoireConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloc_operatoire'

def ready(self):
    import consultations.signals  # ou bloc_operatoire.signals
