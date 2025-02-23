from telebot.handler_backends import State, StatesGroup


class AuthStates(StatesGroup):
    username = State()
    password = State()


class MenuStates(StatesGroup):
    menu = State()
    create_product = State()
    delete_product = State()
    update_product = State()
    inventory = State()
    search_product = State()
