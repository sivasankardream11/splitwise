from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    AppConfig class for the user app.

    This class represents the configuration for the user app.

    Attributes:
        default_auto_field (str): The default auto field for database models.
        name (str): The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
