from django.apps import AppConfig


class HappyShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happy_shop'

    def ready(self) -> None:
        from . import signals