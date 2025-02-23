from telebot.types import KeyboardButton, ReplyKeyboardMarkup


class BotButton:
    CREATE_PRODUCT = '➕ Добавить продукт'
    DELETE_PRODUCT = '❌ Удалить продукт'
    SEARCH_PRODUCT = '🔍 Поиск продукта'
    PRODUCT_INVENTORY = '📦 Склад'


def get_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Создаем клавиатуру
    keyboard.add(
        KeyboardButton(BotButton.CREATE_PRODUCT),
        KeyboardButton(BotButton.DELETE_PRODUCT),
        KeyboardButton(BotButton.SEARCH_PRODUCT),
        KeyboardButton(BotButton.PRODUCT_INVENTORY)
    )
    return keyboard

