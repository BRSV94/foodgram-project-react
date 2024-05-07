from django.contrib import admin

from .models import (Ingredient, IngredientInRecipe,
                     MeasurementUnit, Recipe, Tag)


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
    raw_id_fields = (
        'ingredients',
    )
    inlines = (
        IngredientInRecipeInline,
    )

    @admin.display(description='ингредиенты')
    def ingredients_list(self, obj):
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
        'recipe',
        'amount',
    )
    list_filter = (
        'ingredient',
    )
    search_fields = (
        'ingredient__name',
    )

    # @admin.display(description='Используется в:')
    # def recipes_list(self, obj):
    #     print(obj.recipe)
    #     return ', '.join([recipe.name for recipe in obj.recipe]) or None


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'color',
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
