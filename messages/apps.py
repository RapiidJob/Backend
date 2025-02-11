from django.apps import AppConfig


class MessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messages'
    label = "notifications"
    
    def ready(self):
        import messages.signals  # noqa