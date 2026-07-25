from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AmazonConfig(AppConfig):
    name = 'amazon'
    def ready(self):
        from amazon.signals import create_groups_permissions
        post_migrate.connect(create_groups_permissions)
