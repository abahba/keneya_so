from django.apps import AppConfig


class SoinsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'soins'

def ready(self):
    import consultations.signals