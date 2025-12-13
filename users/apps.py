from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the users app.
    Handles user authentication, registration, and verification.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'User Management'
