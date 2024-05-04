from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.settings import EMAIL_MAX_LENGTH, USERS_FIELDS_MAX_LENGTH


class User(AbstractUser):
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        blank=False,
        verbose_name='Email',
        unique=True,
    )
    first_name = models.CharField(
        max_length=USERS_FIELDS_MAX_LENGTH,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=USERS_FIELDS_MAX_LENGTH,
        blank=False,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=USERS_FIELDS_MAX_LENGTH,
        blank=False,
        verbose_name='Пароль'
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class UsersSubscribes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь',
    )
    subscribes = models.ManyToManyField(
        User,
        related_name='subscribes',
        verbose_name='Подписки',
        blank=True,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorited(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Пользователь',
    )
    recipes = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorite_in',
        verbose_name='Рецепты',
        blank=True
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipes = models.ManyToManyField(
        'recipes.Recipe',
        related_name='in_shopping_cart',
        verbose_name='Рецепты',
        blank=True,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
