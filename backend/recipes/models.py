from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
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


class MeasurementUnit(models.Model):
    measurement_unit = models.CharField(
        max_length=200,
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
        max_length=200,
        verbose_name='Ингридиент',
    )
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.CASCADE,
        related_name='ingredients',
        # default='шт.'
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']
        unique_together = ('name', 'measurement_unit',)

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
        max_length=200,
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
    #     Ingredient,
    #     through='IngredientInRecipe',
    #     related_name='recipes',
    #     verbose_name='Ингридиенты',
    #     blank=True,
    # )
    ingredients = models.ManyToManyField(
        'IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты',
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги',
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления в мин.',
        null = False,
        help_text = ('Время приготовления должно быть указано в минутах. '
                     'Это поле не может иметь отрицительные и нулевое значения.') 
    )
    

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    # recipe = models.ForeignKey(
    #     Recipe,
    #     on_delete=models.CASCADE,
    #     related_name='ingredient_in_recipe',
    # )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        ordering = ['ingredient']
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['recipe', 'ingredient'],
        #         name='unique_recipe_ingredient'
        #     )
        # ]

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'
