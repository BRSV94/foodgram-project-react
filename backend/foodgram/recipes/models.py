from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тэг',
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='Цвет',
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Ингридиент',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингридиенты',
        )
    is_favorited = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.CharField(
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.TimeField()

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']

    def __str__(self):
        return self.name

