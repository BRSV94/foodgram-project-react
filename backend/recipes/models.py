from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models

from foodgram.constants import (COLOR_FIELDS_MAX_LENGTH, MAX_POSITIVE_VALUE,
                                MIN_POSITIVE_VALUE, RECIPES_MAX_LENGTH)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=RECIPES_MAX_LENGTH,
        blank=False,
        verbose_name='Тэг',
    )
    color = models.CharField(
        max_length=COLOR_FIELDS_MAX_LENGTH,
        blank=False,
        null=True,
        verbose_name='Цвет',
        validators=[
            RegexValidator(
                regex='^#[A-Fa-f0-9]{6}$',
                message=('Цвет должен быть указан в формате '
                         '"#XXXXXX", где "X" - любая цифра '
                         'или буква латинского алфавита.'),
            ),
        ],
    )
    slug = models.CharField(
        max_length=RECIPES_MAX_LENGTH,
        blank=False,
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message=('Slug может содержать только'
                         'буквенные и цифровые символы.'),
            ),
        ],
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class MeasurementUnit(models.Model):
    measurement_unit = models.CharField(
        max_length=RECIPES_MAX_LENGTH,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ['measurement_unit']

    def __str__(self) -> str:
        return self.measurement_unit


class Ingredient(models.Model):
    name = models.CharField(
        max_length=RECIPES_MAX_LENGTH,
        verbose_name='Ингридиент',
    )
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        null=True,
    )
    name = models.CharField(
        max_length=RECIPES_MAX_LENGTH,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение',
        null=False,
        blank=False,
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    # ingredients = models.ManyToManyField(
    #     'IngredientInRecipe',
    #     related_name='recipes',
    #     verbose_name='Ингредиенты',
    #     blank=True,
    # )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги',
        null=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_POSITIVE_VALUE),
            MaxValueValidator(MAX_POSITIVE_VALUE),
        ],
        verbose_name='Время приготовления в мин.',
        null=False,
        help_text=('Время приготовления должно быть указано в минутах. '
                     'Это поле не может иметь '
                     'отрицительные и нулевое значения.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
    )
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(MIN_POSITIVE_VALUE),
            MaxValueValidator(MAX_POSITIVE_VALUE),
        ]
    )

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        ordering = ['ingredient']

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'
