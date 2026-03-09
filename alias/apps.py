from django.apps import AppConfig


class AliasConfig(AppConfig):
    name = "alias"

    def ready(self):
        import alias.documents