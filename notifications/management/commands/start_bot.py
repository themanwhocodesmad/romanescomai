from django.core.management.base import BaseCommand
from romanesco.telegram_bot import run_bot


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Telegram Bot...")
        run_bot()
