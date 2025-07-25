from django.apps import AppConfig


class TheatersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'theaters'

    def ready(self):
        import theaters.signals
