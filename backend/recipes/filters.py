from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    # tags = filters.ModelMultipleChoiceFilter(
    #     field_name='tags__slug',
    #     to_field_name='slug',
    #     queryset=Tag.objects.all(),
    # )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(
        # method='filter_is_favorited's
        method='filter_boolean_field',
        # extra_param='favorites',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        # method='filter_is_in_shopping_cart'
        method='filter_boolean_field',
        # extra_param='shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    # def filter_is_favorited(self, queryset, name, value):
    #     user = self.request.user
    #     if value and not user.is_anonymous:
    #         return queryset.filter(favorites__user=user)
    #     return queryset

    # def filter_is_in_shopping_cart(self, queryset, name, value):
    #     user = self.request.user
    #     if value and not user.is_anonymous:
    #         return queryset.filter(shopping_cart__user=user)
    #     return queryset
    
    def filter_boolean_field(self, queryset, name, value):
        user = self.request.user
        field_params = {
            'is_favorited': 'favoristes',
            'is_in_shopping_cart': 'in_shopping_cart'
        }
        print('LOL'*99)
        print(name)
        if value and not user.is_anonymous:
            filter_kwargs = {f'{field_params[name]}__user': user}
            return queryset.filter(**filter_kwargs)
        return queryset
    

class IngredientFilter(FilterSet):
    # name = filters.CharFilter(lookup_expr='startswith')
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
