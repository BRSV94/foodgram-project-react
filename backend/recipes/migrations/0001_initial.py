# Generated by Django 3.2.3 on 2024-04-23 18:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Ингридиент')),
            ],
            options={
                'verbose_name': 'ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецепте',
                'ordering': ['ingredient'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'единица измерения',
                'verbose_name_plural': 'Единицы измерения',
                'ordering': ['measurement_unit'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='recipes/images/', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.PositiveIntegerField(help_text='Время приготовления должно быть указано в минутах. Это поле не может иметь отрицительные и нулевое значения.', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления в мин.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Тэг')),
                ('color', models.CharField(max_length=7, null=True, verbose_name='Цвет')),
                ('slug', models.CharField(max_length=200, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Slug can only contain lettersand digits characters.', regex='^[-a-zA-Z0-9_]+$')])),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ['name'],
            },
        ),
    ]
