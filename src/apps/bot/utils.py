from PIL.ImageCms import buildProofTransform

from apps.products.models import Product
from apps.users.models import BotUser, User


def get_user(tg_user_id) -> BotUser | None:
    bot_user = BotUser.objects.select_related('user').filter(tg_user_id=tg_user_id).first()
    return bot_user


def is_authenticated(tg_user_id):
    return BotUser.objects.filter(tg_user_id=tg_user_id).exists()


def check_username(username: str) -> bool:
    return User.objects.filter(username=username).exists()


def bot_authenticate(username: str, password: str, tg_user_id: int) -> BotUser | None:
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            bot_user, _ = BotUser.objects.get_or_create(user=user, tg_user_id=tg_user_id)
            return bot_user
        return None
    except Exception as e:
        return None


def get_product(name: str) -> Product | None:
    product = Product.objects.filter(name=name).first()
    return product


def check_product(name: str) -> bool:
    return Product.objects.filter(name=name).exists()


def create_product(name: str) -> Product:
    product, _ = Product.objects.get_or_create(name=name)
    return product


def delete_product(name: str) -> None:
    Product.objects.filter(name=name).delete()
