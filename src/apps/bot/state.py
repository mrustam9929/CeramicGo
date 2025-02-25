from telebot.handler_backends import State, StatesGroup


class AuthStates(StatesGroup):
    username = State()
    password = State()


class MenuStates(StatesGroup):
    menu = State()
    create_product = State()
    delete_product = State()
    select_update_product = State()
    update_product = State()
    inventory = State()
    inventory_count = State()
    inventory_price = State()
    inventory_operation_type = State()
    inventory_confirm = State()
    product_info = State()
