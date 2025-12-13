from django.apps import AppConfig


class ItemsConfig(AppConfig):
    """
    Configuration for the items app.
    Handles lost & found items management.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'items'
    verbose_name = 'Lost & Found Items'
