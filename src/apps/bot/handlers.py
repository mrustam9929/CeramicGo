from apps.bot.config import bot
from apps.bot.keyboards import get_menu_keyboard, BotButton
from apps.bot.state import AuthStates, MenuStates
from apps.bot.utils import is_authenticated, check_username, bot_authenticate, check_product, delete_product
from apps.products.models import Product


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_authenticated(user_id):
        bot.set_state(message.chat.id, MenuStates.menu)
        bot.send_message(message.chat.id, 'Меню', reply_markup=get_menu_keyboard())
    else:
        bot.send_message(message.chat.id, 'Введите логин:')
        bot.set_state(message.chat.id, AuthStates.username)


@bot.message_handler(state=AuthStates.username)
def get_username(message):
    if check_username(message.text):
        with bot.retrieve_data(message.chat.id) as data:
            data['username'] = message.text
        bot.set_state(message.chat.id, AuthStates.password)
        bot.send_message(message.chat.id, "Введите пароль:")
    else:
        bot.send_message(message.chat.id, 'Неверные данные')


@bot.message_handler(state=AuthStates.password)
def get_password(message):
    with bot.retrieve_data(message.chat.id) as data:
        username = data['username']
        password = message.text
        user = bot_authenticate(username=username, password=password, tg_user_id=message.from_user.id)
        if user:
            bot.send_message(message.chat.id, f'Добро пожаловать {user.user.username}',
                             reply_markup=get_menu_keyboard())
            bot.set_state(message.chat.id, MenuStates.menu)
        else:
            bot.send_message(message.chat.id, "❌ Ошибка! Неверный логин или пароль.\nПопробуйте снова: /start")
            bot.delete_state(message.chat.id)


@bot.message_handler(state=MenuStates.menu)
def menu(message):
    if message.text == BotButton.CREATE_PRODUCT:
        bot.set_state(message.chat.id, MenuStates.create_product)
        bot.send_message(message.chat.id, 'Введите название продукта:')
    elif message.text == BotButton.DELETE_PRODUCT:
        bot.set_state(message.chat.id, MenuStates.delete_product)
        bot.send_message(message.chat.id, 'Введите название продукта чтобы УДАЛИТЬ:')
    elif message.text == BotButton.SEARCH_PRODUCT:
        pass
    elif message.text == BotButton.PRODUCT_INVENTORY:
        pass


@bot.message_handler(state=MenuStates.create_product)
def create_product(message):
    name = message.text
    if check_product(name):
        bot.send_message(message.chat.id, 'Продукт уже существует', reply_markup=get_menu_keyboard())
    else:
        create_product(name)
        bot.send_message(message.chat.id, 'Продукт добавлен', reply_markup=get_menu_keyboard())
    bot.set_state(message.chat.id, MenuStates.menu)


@bot.message_handler(state=MenuStates.delete_product)
def delete_product(message):
    name = message.text
    if check_product(name):
        delete_product(name)
        bot.send_message(message.chat.id, 'Продукт удален', reply_markup=get_menu_keyboard())
    bot.set_state(message.chat.id, MenuStates.menu)
