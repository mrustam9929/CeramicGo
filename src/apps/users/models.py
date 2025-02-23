from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "username"

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class BotUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bot_users')
    tg_user_id = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bot_users'
