from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class BotButton:
    CREATE_PRODUCT = '➕ Добавить продукт'
    DELETE_PRODUCT = '❌ Удалить продукт'
    SEARCH_PRODUCT = '🔍 Поиск продукта'
    UPDATE_PRODUCT = '🔄 Обновление товара'
    PRODUCT_INVENTORY = '📦 Склад'
    INVENTORY_RECEIPT = '📥 Поступление'
    INVENTORY_SALE = '💰 Продажа'
    INVENTORY_DEFECT = '⚠️ Брак'
    INVENTORY_CONFIRM = '✅ Подтвердить'
    INVENTORY_CANCEL = '❌ Отменить'


INVENTORY_CONFIRM_MESSAGE_TEMPLATE = """
========================================
Товар: {product_name} 
Тип: {operation_type} 
Кол-во: {count}
Цена: {price} 
========================================
"""

PRODUCT_INFO_TEMPLATE = """
========================================
Товар: {product_name} 
Кол-во: {count}
Цена: {price} 
========================================
"""


def get_inventory_operation_type_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Создаем клавиатуру
    keyboard.add(
        KeyboardButton(BotButton.INVENTORY_RECEIPT),
        KeyboardButton(BotButton.INVENTORY_SALE),
        KeyboardButton(BotButton.INVENTORY_DEFECT)

    )
    return keyboard


def get_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Создаем клавиатуру
    keyboard.add(
        KeyboardButton(BotButton.SEARCH_PRODUCT),
        KeyboardButton(BotButton.PRODUCT_INVENTORY),
        KeyboardButton(BotButton.CREATE_PRODUCT),
        KeyboardButton(BotButton.DELETE_PRODUCT),
        KeyboardButton(BotButton.UPDATE_PRODUCT),

    )
    return keyboard


def get_inventory_operation_confirm_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Создаем клавиатуру
    keyboard.add(
        KeyboardButton(BotButton.INVENTORY_CONFIRM),
        KeyboardButton(BotButton.INVENTORY_CANCEL)

    )
    return keyboard


def get_search_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔍 Найти товар", switch_inline_query_current_chat=""))
    return keyboard
