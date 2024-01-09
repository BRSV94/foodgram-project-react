from django.db import models
from django.core.validators import RegexValidator
from users.models import User


class Tag(models.Model):
    title = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Тэг',
    )
    color = models.CharField(
        max_length=7,
        blank=False,
        null=True,
        verbose_name='Цвет',
    )
    slug = models.CharField(
        max_length=200,
        blank=False,
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message=('Slug can only contain letters'
                         'and digits characters.'),
            ),
        ],
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Ингридиент',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
    )
    quantity = models.FloatField()

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.CharField(
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингридиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги',
    )
    cooking_time = models.TimeField(
        verbose_name='Время приготовления в мин.',
    )
    

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Favorited(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorited',
        verbose_name='Изранное',
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='in_favorites',
        verbose_name='В избранном',
    )

