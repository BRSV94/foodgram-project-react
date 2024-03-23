import base64

import webcolors
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.db.models import Count
from django.shortcuts import get_object_or_404
from recipes.models import (Ingredient, IngredientInRecipe, MeasurementUnit,
                            Recipe, Tag)
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, Field, ImageField,
                                        ListSerializer, ModelSerializer,
                                        PrimaryKeyRelatedField, RelatedField,
                                        SerializerMethodField,
                                        StringRelatedField, ValidationError)
from users.models import Favorited, User, UsersSubscribes


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
    

class Hex2NameColor(Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise ValidationError('Для этого цвета нет имени')
        return data


class UserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj, *args, **kwargs):
        user = obj

        if not self.context.get('request'):
            return True

        current_user = self.context.get('request').user
        return UsersSubscribes.objects.filter(
            user=current_user.id, subscribes=user).exists()
            # user=current_user).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('id',)

class UserCreateSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
        read_only_fields = ('id', 'is_subscribed')


class TagSerializer(ModelSerializer):

    color = Hex2NameColor()
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('name', 'color', 'slug',)


class IngredientSerializer(ModelSerializer):
    measurement_unit = SerializerMethodField()

    def get_measurement_unit(self, obj):
        return str(obj.measurement_unit)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('id', 'name', 'measurement_unit',)


class IngredientInRecipeSerializer(ModelSerializer):
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()

    def get_name(self, obj):
        return obj.ingredient.name
    
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit.measurement_unit


    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class TagListField(PrimaryKeyRelatedField):
    def to_representation(self, value):
        return {'id': value.id, 'name': value.name,
                'color': value.color, 'slug': value.slug}


class RecipeSerializer(ModelSerializer):
    tags = TagListField(queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True, read_only=True,
                                               source='ingredient_in_recipe')
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',)
        read_only_fields = ('id', 'author', 'is_favorited', 'is_in_shopping_cart',)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated and
                user.favorited.filter(recipes=obj).exists())
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated and
                user.shopping_cart.filter(recipes=obj).exists())


class FavoritedSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_fields = ('id', 'name', 'image', 'cooking_time',)

    # def create(self, validated_data):
    #     user = self.context.get('request').user
    #     recipe_id = self.context.get('view').kwargs.get('recipe_id') # View?
    #     recipe = get_object_or_404(Recipe, id=recipe_id)
    #     obj, create = Favorited.objects.get_or_create(user=user)
    #     obj.recipes.add(recipe)
    #     return recipe


class SubRecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class SubscribesSerializer(UserSerializer):
    recipes = SubRecipeSerializer(read_only=True, many=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count',)
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed', 'recipes',
                            'recipes_count')
        depth = 1


    def get_recipes_count(self, obj):
        return obj.recipes.count()
    
    # def validate_recipes(self, queryset):
    #     recipes_limit = int(self.context['request'].query_params['recipes_limit'])
    #     print(recipes_limit)
    #     print(queryset[:recipes_limit])
    #     return queryset[:recipes_limit]
