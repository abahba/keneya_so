from django.apps import AppConfig


class ImagerieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'imagerie'

def ready(self):
    import imagerie.signals  # ajuste selon ton app
