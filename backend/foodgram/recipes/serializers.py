from rest_framework.serializers import ModelSerializer
from .models import Recipe, Tag, Ingredient


class TagSerializer(ModelSerializer):
    pass


class IngredientSerializer(ModelSerializer):
    pass


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    Ingredient = IngredientSerializer(many=True)


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',)
        read_only_fields = ('id', 'author', 'is_favorited', 'is_in_shopping_cart',)


class FavoritesSerializer(ModelSerializer):
    pass

