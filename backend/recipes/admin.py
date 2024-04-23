from django.contrib import admin

from .models import (
    Ingredient, IngredientInRecipe,
    MeasurementUnit, Recipe, Tag,
)


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
        'recipes',
        'amount',
    )
    list_filter = (
        'ingredient',
    )
    search_fields = (
        'ingredient',
    )

    @admin.display(description='Используется в:')
    def recipes(self):
        return f'{self}, LOLKEK'
    # return ', '.join([recipe.name for recipe in self.recipes.all()]) or None



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
