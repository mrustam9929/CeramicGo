from PIL.ImageCms import buildProofTransform
from django.db.models import QuerySet

from apps.bot.keyboards import BotButton
from apps.products.models import Product, ProductInventoryOperation
from apps.users.models import BotUser, User


class BotHelper:
    @staticmethod
    def get_user(tg_user_id) -> BotUser | None:
        bot_user = BotUser.objects.select_related('user').filter(tg_user_id=tg_user_id).first()
        return bot_user

    @staticmethod
    def is_authenticated(tg_user_id):
        return BotUser.objects.filter(tg_user_id=tg_user_id).exists()

    @staticmethod
    def check_username(username: str) -> bool:
        return User.objects.filter(username=username).exists()

    @staticmethod
    def bot_authenticate(username: str, password: str, tg_user_id: int) -> BotUser | None:
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                bot_user, _ = BotUser.objects.get_or_create(user=user, tg_user_id=tg_user_id)
                return bot_user
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_product(name: str) -> Product | None:
        product = Product.objects.filter(name=name).first()
        return product

    @staticmethod
    def check_product(name: str) -> bool:
        return Product.objects.filter(name=name).exists()

    @staticmethod
    def create_product(name: str) -> Product:
        product, _ = Product.objects.get_or_create(name=name)
        return product

    @staticmethod
    def delete_product(name: str) -> None:
        Product.objects.filter(name=name).delete()

    @staticmethod
    def update_product(name: str, product: Product) -> None:
        product.name = name
        product.save(update_fields=['name', ])

    @classmethod
    def check_product_availability(cls, product_name: str, count: int) -> bool:
        product = cls.get_product(product_name)
        return product.count >= count

    @staticmethod
    def get_inventory_type(operation_type: str) -> str:
        if operation_type == BotButton.INVENTORY_SALE:
            _type = ProductInventoryOperation.OperationType.SALE
        elif operation_type == BotButton.INVENTORY_DEFECT:
            _type = ProductInventoryOperation.OperationType.DEFECT
        elif operation_type == BotButton.INVENTORY_RECEIPT:
            _type = ProductInventoryOperation.OperationType.RECEIPT
        else:
            raise Exception(f'Unknown operation type: {operation_type}')
        return _type

    @classmethod
    def confirm_product_inventory(cls, product_name: str, operation_type: str, count: int, price: str,
                                  bot_user_id: int) -> None:
        ProductInventoryOperation.objects.create(
            user_id=cls.get_user(bot_user_id).user_id,
            product=cls.get_product(product_name),
            operation_type=operation_type,
            count=count,
            price=price,
        )

    @staticmethod
    def get_similar_products(query_str) -> QuerySet:
        products = Product.objects.filter(name__icontains=query_str)
        return products
