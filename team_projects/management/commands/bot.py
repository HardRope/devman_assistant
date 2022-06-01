from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        pass