import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Устанавливает вебхук для Telegram-бота"

    def handle(self, *args, **kwargs):
        bot_token = settings.TG_BOT_TOKEN
        webhook_url = settings.TG_WEBHOOK_URL
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        response = requests.post(url, data={"url": webhook_url})

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS("Вебхук успешно установлен!"))
        else:
            self.stderr.write(f"Ошибка при установке вебхука: {response.text}")
