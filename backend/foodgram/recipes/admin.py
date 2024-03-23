from django.contrib import admin

from .models import (Ingredient, IngredientInRecipe, MeasurementUnit, Recipe,
                     Tag)


class TagsInline(admin.TabularInline):
    model = Tag


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    filter_horizontal = (
        'tags',
    )
    inlines = (
        IngredientInRecipeInline,
    )


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )
    list_filter = (
        'name',
    )
    inlines = (
        IngredientInRecipeInline,
    )


@admin.register(IngredientInRecipe)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
    )
    list_filter = (
        'ingredient',
    )


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_filter = (
        'name',
        'slug',
    )


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = (
        'measurement_unit',
    )
    list_filter = (
        'measurement_unit',
    )


# class IngredientsInline(admin.TabularInline):
#     model = IngredientInRecipe
#     min_num = 1


class TagsInline(admin.TabularInline):
    model = Tag


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1
