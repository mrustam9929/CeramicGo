from telebot.types import ReplyKeyboardRemove, InlineQueryResultArticle, InputTextMessageContent, BotCommand

from apps.bot.config import bot
from apps.bot.keyboards import PRODUCT_INFO_TEMPLATE
from apps.bot.keyboards import get_menu_keyboard, BotButton, get_inventory_operation_type_keyboard, \
    get_inventory_operation_confirm_keyboard, INVENTORY_CONFIRM_MESSAGE_TEMPLATE, get_search_keyboard
from apps.bot.state import AuthStates, MenuStates
from apps.bot.utils import BotHelper


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if BotHelper.is_authenticated(user_id):
        bot.set_state(message.chat.id, MenuStates.menu)
        bot.send_message(message.chat.id, 'Меню', reply_markup=get_menu_keyboard())
    else:
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.chat.id, AuthStates.username)


@bot.message_handler(commands=['menu'])
def menu_command(message):
    user_id = message.from_user.id
    if BotHelper.is_authenticated(user_id):
        bot.set_state(message.chat.id, MenuStates.menu)
        bot.send_message(message.chat.id, 'Меню', reply_markup=get_menu_keyboard())
    else:
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.chat.id, AuthStates.username)


@bot.message_handler(state=AuthStates.username)
def get_username(message):
    if BotHelper.check_username(message.text):
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
        user = BotHelper.bot_authenticate(username=username, password=password, tg_user_id=message.from_user.id)
        if user:
            bot.send_message(message.chat.id, f'Добро пожаловать {user.user.username}',
                             reply_markup=get_menu_keyboard())
            bot.set_state(message.chat.id, MenuStates.menu)
        else:
            bot.send_message(message.chat.id, "❌ Ошибка! Неверный логин или пароль.\nПопробуйте снова: /start")
            bot.delete_state(message.chat.id)


@bot.message_handler(state=MenuStates.product_info)
def get_product_info(message):
    product = BotHelper.get_product(message.text)
    if product is None:
        bot.send_message(message.chat.id, 'Продукт не найден')
    else:
        product_info = PRODUCT_INFO_TEMPLATE.format(
            product_name=product.name,
            price=product.price,
            count=product.count
        )
        bot.send_message(message.chat.id, product_info)


@bot.message_handler(state=MenuStates.menu)
def menu(message):
    if not BotHelper.is_authenticated(message.from_user.id):
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.chat.id, AuthStates.username)
        return

    if message.text == BotButton.CREATE_PRODUCT:
        bot.set_state(message.chat.id, MenuStates.create_product)
        bot.send_message(message.chat.id, 'Введите название товара:', reply_markup=get_search_keyboard())
    elif message.text == BotButton.DELETE_PRODUCT:
        bot.set_state(message.chat.id, MenuStates.delete_product)
        bot.send_message(message.chat.id, 'Введите название товара чтобы УДАЛИТЬ:', reply_markup=get_search_keyboard())
    elif message.text == BotButton.UPDATE_PRODUCT:
        bot.set_state(message.chat.id, MenuStates.select_update_product)
        bot.send_message(message.chat.id, 'Введите название товара:', reply_markup=get_search_keyboard())
    elif message.text == BotButton.SEARCH_PRODUCT:
        bot.set_state(message.chat.id, MenuStates.product_info)
        bot.send_message(message.chat.id, 'Введите название товара:', reply_markup=get_search_keyboard())
    elif message.text == BotButton.PRODUCT_INVENTORY:
        bot.set_state(message.chat.id, MenuStates.inventory)
        bot.send_message(message.chat.id, 'Введите название товара:', reply_markup=get_search_keyboard())


@bot.message_handler(state=MenuStates.create_product)
def create_product(message):
    if not BotHelper.is_authenticated(message.from_user.id):
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.chat.id, AuthStates.username)
        return
    name = message.text
    if BotHelper.check_product(name):
        bot.send_message(message.chat.id, 'Товар уже существует', reply_markup=get_menu_keyboard())
    else:
        BotHelper.create_product(name)
        bot.send_message(message.chat.id, 'Товар добавлен', reply_markup=get_menu_keyboard())
    bot.set_state(message.chat.id, MenuStates.menu)


@bot.message_handler(state=MenuStates.delete_product)
def delete_product(message):
    if not BotHelper.is_authenticated(message.from_user.id):
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.chat.id, AuthStates.username)
        return
    name = message.text
    if BotHelper.check_product(name):
        BotHelper.delete_product(name)
        bot.send_message(message.chat.id, 'Товар удален', reply_markup=get_menu_keyboard())
    else:
        bot.send_message(message.chat.id, 'Товар не найден', reply_markup=get_menu_keyboard())
    bot.set_state(message.chat.id, MenuStates.menu)


@bot.message_handler(state=MenuStates.select_update_product)
def select_update_product(message):
    if not BotHelper.is_authenticated(message.from_user.id):
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.chat.id, AuthStates.username)
        return
    name = message.text
    product = BotHelper.get_product(name)
    if product is None:
        bot.set_state(message.chat.id, MenuStates.menu)
        bot.send_message(message.chat.id, 'Товар не найден', reply_markup=get_menu_keyboard())
    else:
        with bot.retrieve_data(message.chat.id) as data:
            data['update_product'] = product.name
        bot.set_state(message.chat.id, MenuStates.update_product)
        bot.send_message(message.chat.id, 'Введите новое название товара:')


@bot.message_handler(state=MenuStates.update_product)
def update_product(message):
    new_name = message.text
    with bot.retrieve_data(message.chat.id) as data:
        product = BotHelper.get_product(data['update_product'])
        if product is None:
            bot.send_message(message.chat.id, 'Товар не найден', reply_markup=get_menu_keyboard())
        else:
            BotHelper.update_product(new_name, product)
            bot.send_message(message.chat.id, 'Товар обновлен', reply_markup=get_menu_keyboard())
    bot.set_state(message.chat.id, MenuStates.menu)


@bot.message_handler(state=MenuStates.inventory)
def inventory_product_select(message):
    if not BotHelper.is_authenticated(message.from_user.id):
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.chat.id, AuthStates.username)
        return
    product_name = message.text
    if BotHelper.check_product(product_name):
        with bot.retrieve_data(message.chat.id) as data:
            data['inventory__product_name'] = product_name
        bot.set_state(message.chat.id, MenuStates.inventory_operation_type)
        bot.send_message(message.chat.id, 'Тип:', reply_markup=get_inventory_operation_type_keyboard())

    else:
        bot.send_message(message.chat.id, 'Товар не найден')


@bot.message_handler(state=MenuStates.inventory_operation_type)
def inventory_operation_type(message):
    operation_type = message.text
    if operation_type in (BotButton.INVENTORY_DEFECT, BotButton.INVENTORY_RECEIPT, BotButton.INVENTORY_SALE):
        with bot.retrieve_data(message.chat.id) as data:
            data['inventory__operation_type'] = operation_type
        bot.set_state(message.chat.id, MenuStates.inventory_count)
        bot.send_message(message.chat.id, 'Кол-во товара:', reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Укажите правильный тип',
                         reply_markup=get_inventory_operation_type_keyboard())


@bot.message_handler(state=MenuStates.inventory_count)
def inventory_product_count(message):
    product_count = message.text
    if not product_count.isdigit() or int(product_count) < 1:
        bot.send_message(message.chat.id, 'Неверный формат, Укажите кол-во товара:')
        return
    product_count = int(product_count)
    with bot.retrieve_data(message.chat.id) as data:
        operation_type = data['inventory__operation_type']
        if operation_type != BotButton.INVENTORY_RECEIPT:
            product_name = data['inventory__product_name']
            if not BotHelper.check_product_availability(product_name, product_count):
                bot.send_message(message.chat.id, 'Не хватает товара на складе!')
                return
        data['inventory__count'] = product_count
        bot.set_state(message.chat.id, MenuStates.inventory_price)
        bot.send_message(message.chat.id, 'Цена:')


@bot.message_handler(state=MenuStates.inventory_price)
def inventory_price(message):
    product_price = message.text
    if not product_price.isdigit() or int(product_price) < 0:
        bot.send_message(message.chat.id, 'Неверный формат, Укажите цену товара:')
    else:
        with bot.retrieve_data(message.chat.id) as data:
            data['inventory__price'] = product_price
            bot.set_state(message.chat.id, MenuStates.inventory_confirm)
            bot.send_message(
                message.chat.id,
                INVENTORY_CONFIRM_MESSAGE_TEMPLATE.format(
                    product_name=data['inventory__product_name'],
                    operation_type=data['inventory__operation_type'],
                    count=data['inventory__count'],
                    price=data['inventory__price'],

                ),
                reply_markup=get_inventory_operation_confirm_keyboard()
            )


@bot.message_handler(state=MenuStates.inventory_confirm)
def inventory_confirm(message):
    if message.text == BotButton.INVENTORY_CONFIRM:
        with bot.retrieve_data(message.chat.id) as data:
            product_name = data['inventory__product_name']
            operation_type = BotHelper.get_inventory_type(data['inventory__operation_type'])
            count = data['inventory__count']
            price = data['inventory__price']

            has_product = BotHelper.check_product(product_name)
            is_receipt = data['inventory__operation_type'] == BotButton.INVENTORY_RECEIPT
            is_available = is_receipt or BotHelper.check_product_availability(product_name, count)
            if has_product and is_available:
                bot_user_id = message.from_user.id
                BotHelper.confirm_product_inventory(product_name, operation_type, count, price, bot_user_id)
                bot.send_message(message.chat.id, 'Сохранено', reply_markup=get_menu_keyboard())
            else:
                bot.send_message(message.chat.id, 'Ошибка проверьте продукт или кол-во',
                                 reply_markup=get_menu_keyboard())
    else:
        bot.send_message(message.chat.id, 'Отменено', reply_markup=get_menu_keyboard())
    with bot.retrieve_data(message.chat.id) as data:
        data.clear()
    bot.set_state(message.chat.id, MenuStates.menu)


@bot.inline_handler(lambda query: len(query.query) > 0 and query.chat_type == "sender")
def search_query(query):
    query_str = query.query.lower()
    products = BotHelper.get_similar_products(query_str)

    results = []
    for product in products:
        results.append(
            InlineQueryResultArticle(
                id=str(product.id),
                title=f'{product.name}',
                description='',
                input_message_content=InputTextMessageContent(message_text=product.name),
            )
        )

    bot.answer_inline_query(query.id, results)
