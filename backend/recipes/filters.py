from django_filters.rest_framework import BooleanFilter, FilterSet

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(
        method='filter_is_favorited',
        label='Избранное',
    )
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart',
        label='Список покупок',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorited__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset
    

class IngredientFilter(FilterSet):

    class Meta:
        model = Ingredient
        fields = ('name',)
