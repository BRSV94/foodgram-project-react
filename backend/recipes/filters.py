from django_filters.rest_framework import (BooleanFilter, FilterSet,
                                           ModelMultipleChoiceFilter)

from .models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(
        method='filter_is_favorited',
        label='Избранное',
    )
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart',
        label='Список покупок',
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorite_in__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(in_shopping_cart__user=user)
        return queryset


class IngredientFilter(FilterSet):

    class Meta:
        model = Ingredient
        fields = ('name',)
