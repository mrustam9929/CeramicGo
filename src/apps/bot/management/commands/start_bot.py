from django.core.management import BaseCommand
from apps.bot.handlers import bot

class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.infinity_polling()
