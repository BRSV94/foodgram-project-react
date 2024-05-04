from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_boolean_field',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_boolean_field',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_boolean_field(self, queryset, name, value):
        user = self.request.user
        field_params = {
            'is_favorited': 'favorite_in',
            'is_in_shopping_cart': 'in_shopping_cart'
        }
        if value and not user.is_anonymous:
            filter_kwargs = {f'{field_params[name]}__user': user}
            return queryset.filter(**filter_kwargs)
        return queryset


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
