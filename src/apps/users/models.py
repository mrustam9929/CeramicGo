from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "username"

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
