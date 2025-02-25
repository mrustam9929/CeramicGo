import telebot
from django.conf import settings
from telebot.custom_filters import StateFilter

from telebot.storage import StateRedisStorage
from telebot.types import BotCommand

bot = telebot.TeleBot(
    settings.TG_BOT_TOKEN,
    state_storage=StateRedisStorage(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=1
    )
)
bot.add_custom_filter(StateFilter(bot))
bot.set_my_commands([
    BotCommand("start", "Перезагрузить"),
    BotCommand("menu", "Меню"),
])
