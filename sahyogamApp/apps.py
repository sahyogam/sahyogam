from django.apps import AppConfig


class SahyogamappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sahyogamApp'


from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Sahyogam'

    # def ready(self):
        # from .scheduler import start_scheduler
        # start_scheduler()
