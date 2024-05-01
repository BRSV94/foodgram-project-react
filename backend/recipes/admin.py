from django.contrib import admin
from django.utils.html import format_html

from api.fields import Hex2NameColor
from .models import (Ingredient, IngredientInRecipe,
                     MeasurementUnit, Recipe, Tag)
from .widgets import ColorPickerWidget


class TagsInline(admin.TabularInline):
    model = Tag


class IngredientInline(admin.TabularInline):
    model = Ingredient


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1
    inlines = (
        IngredientInline,
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'ingredients_list',
        'tags_list',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    filter_horizontal = (
        'tags',
    )
    search_fields = (
        'name',
    )

    @admin.display(description='ингредиенты')
    def ingredients_list(self, obj):
        # print(obj.instance.ingredients.all())
        # print(obj.instance.ingredients)
        return ', '.join(
            [str(ingredient) for ingredient in obj.ingredients.all()]
        ) or None

    @admin.display(description='тэги')
    def tags_list(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()]) or None


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    inlines = (
        IngredientInRecipeInline,
    )
    search_fields = (
        'name',
    )


@admin.register(IngredientInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipes_list',
        'amount',
    )
    list_filter = (
        'ingredient',
    )
    search_fields = (
        'ingredient',
    )

    @admin.display(description='Используется в:')
    def recipes_list(self, obj):
        return ', '.join([recipe.name for recipe in obj.recipes.all()]) or None


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    color = {
        Hex2NameColor: {'widget': ColorPickerWidget}
    }
    list_display = (
        'name',
        'slug',
        'color',
    )
    list_filter = (
        'name',
        'slug',
    )

    # def color(self, obj):
    #     return format_html('<span style="color: blue;">{}</span>', obj.some_field)

    # color.short_description = 'цвет'


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = (
        'measurement_unit',
    )
    list_filter = (
        'measurement_unit',
    )
