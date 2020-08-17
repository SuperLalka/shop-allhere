from django.apps import AppConfig


class AppShopConfig(AppConfig):
    name = 'app_shop'

    def ready(self):
        from app_shop import signals
