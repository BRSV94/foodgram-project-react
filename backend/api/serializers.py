from django.contrib.auth.hashers import make_password
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField, ValidationError)

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import User, UsersSubscribes
from .fields import Base64ImageField, Hex2NameColor


class UserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj, *args, **kwargs):
        if not self.context.get('request'):
            return False

        current_user = self.context.get('request').user
        return UsersSubscribes.objects.filter(
            user=current_user.id, subscribes=obj).exists()


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
        read_only_fields = ('id', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class TagSerializer(ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(ModelSerializer):
    measurement_unit = CharField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('name', 'measurement_unit',)


class IngredientInRecipeReadSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeWriteSerializer(IngredientInRecipeReadSerializer):
    id = IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit')

    def validate_id(self, value):
        if not Ingredient.objects.filter(id=value).exists():
            raise ValidationError(
                "Ингредиента с таким id не существует.")
        return value


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeReadSerializer(many=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):

        user = self.context['request'].user
        return (user.is_authenticated
                and user.favorited.filter(recipes=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.shopping_cart.filter(recipes=obj).exists())


class RecipeWriteSerializer(RecipeReadSerializer):
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                  many=True)

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise ValidationError(
                "Необходимо указать ингредиенты.")
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise ValidationError(
                "Ингредиенты не могут повторяться.")
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise ValidationError(
                "Необходимо указать тэги.")
        if len(tags) != len(set(tags)):
            raise ValidationError(
                "Тэги не могут повторяться.")
        return tags

    def recipe_create_or_update(self, validated_data, recipe):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        if not recipe:
            recipe = Recipe.objects.create(**validated_data)

        ingredients = []
        for ingredient_data in ingredients_data:
            ing_id = ingredient_data['id']
            ing_amount = ingredient_data['amount']

            ingredients.append(IngredientInRecipe(
                recipe_id=recipe.id,
                ingredient_id=ing_id,
                amount=ing_amount,
            ))
        ingredients.sort(key=lambda obj: obj.ingredient.name)

        ingredients_objs = IngredientInRecipe.objects.bulk_create(ingredients)
        recipe.ingredients.set(ingredients_objs)
        recipe.tags.set(tags_data)
        return recipe

    def create(self, validated_data):
        recipe = self.recipe_create_or_update(
            validated_data,
            None
        )
        return recipe

    def update(self, instance, validated_data):
        self.validate_tags(validated_data.get('tags'))
        self.validate_ingredients(validated_data.get('ingredients'))
        update_recipe = self.recipe_create_or_update(
            validated_data,
            instance
        )
        return update_recipe

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance=instance,
            context=self.context
        ).data


class SubRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time',)


class SubscribesSerializer(UserSerializer):
    recipes = SubRecipeSerializer(
        read_only=True,
        many=True,
    )
    recipes_count = ReadOnlyField(source='recipes.count')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count',)
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed', 'recipes',
                            'recipes_count')
        depth = 1
