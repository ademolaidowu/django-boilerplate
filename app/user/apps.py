from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.user"
    verbose_name = "Identity and Access Management"

    def ready(self) -> None:
        import app.user.signals
