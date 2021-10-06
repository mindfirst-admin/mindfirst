from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from background_apps.functions import bg_work
        bg_work.start()
