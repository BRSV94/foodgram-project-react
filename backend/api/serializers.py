from django.contrib.auth.hashers import make_password

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from recipes.utils import recipe_create_or_update
from rest_framework.serializers import ReadOnlyField  # ?
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField, ValidationError)
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
            return True

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
        read_only_fields = ('name', 'color', 'slug',)

    def validate_id(self, value):
        if not Tag.objects.filter(id=value).exists():
            raise ValidationError(
                "Тэга с таким id не существует.")
        return value


class IngredientSerializer(ModelSerializer):
    # measurement_unit = SerializerMethodField()
    # measurement_unit = CharField(source='measurement_unit')
    measurement_unit = CharField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('name', 'measurement_unit',)

    def validate_id(self, value):
        if not Ingredient.objects.filter(id=value).exists():
            raise ValidationError(
                "Ингредиента с таким id не существует.")
        return value
    
    def validate_amount(self, value):
        if type(value) != int or value < 1:
            raise ValidationError(
                "Кол-во ингредиента должно быть числом большим нуля.")


    # def get_measurement_unit(self, obj):
    #     return str(obj.measurement_unit)


# class IngredientInRecipeReadSerializer(ModelSerializer):
#     id = IntegerField()
#     amount = IntegerField()
#     # name = SerializerMethodField()
#     # measurement_unit = SerializerMethodField()
#     name = CharField(source='ingredient__name')
#     measurement_unit = CharField(
#         source='ingredient__measurement_unit__measurement_unit'
#     )

#     class Meta:
#         model = IngredientInRecipe
#         fields = ('id', 'name', 'measurement_unit', 'amount')
#         fields = ('name', 'measurement_unit',)


class IngredientInRecipeSerializer(ModelSerializer): # Зачем разделять? Разберись.
    # id = PrimaryKeyRelatedField(queryset=IngredientInRecipe.objects.all()) # А тут id какой модели?
    id = ReadOnlyField(source='ingredient.id') 
    amount = IntegerField()
    # name = SerializerMethodField()
    # measurement_unit = SerializerMethodField()
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit',)

    # def get_name(self, obj):
    #     return obj.ingredient.name

    # def get_measurement_unit(self, obj):
    #     return obj.ingredient.measurement_unit.measurement_unit


# class TagListField(PrimaryKeyRelatedField):
#     def to_representation(self, value):
#         return {'id': value.id, 'name': value.name,
#                 'color': value.color, 'slug': value.slug}


class RecipeReadSerializer(ModelSerializer):
    # tags = TagListField(queryset=Tag.objects.all(), many=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True)
    # ingredients = IngredientInRecipeReadSerializer(many=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    image = Base64ImageField()

    # tags = TagListField(queryset=Tag.objects.all(), many=True)
#     tags = TagSerializer(many=True, read_only=True)
#     author = UserSerializer(read_only=True)
#     ingredients = IngredientInRecipeSerializer(many=True)

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


class RecipeWriteSerializer(ModelSerializer):
    # tags = TagListField(queryset=Tag.objects.all(), many=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True) # Read only?
    ingredients = IngredientInRecipeSerializer(many=True)
    # ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField()


    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        recipe = recipe_create_or_update(
            self,
            validated_data,
            None
        )
        return recipe

    def update(self, instance, validated_data):
        update_recipe = recipe_create_or_update(
            self,
            validated_data,
            instance
        )
        return update_recipe

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise ValidationError(
                "Необходимо указать ингредиенты.")
        if len(list(ingredients)) != len(set(ingredients)):
            raise ValidationError(
                "Ингредиенты не могут повторяться.")
        return ingredients
        # ing_ids = []
        # for ingredient in ingredients:
            # if not ingredient['id'] or not ingredient['amount']:
            #     raise ValidationError(
            #         "Некорректные данные ингредиентов.")
            # if ingredient['id'] in ing_ids:
            #     raise ValidationError(
            #         "Ингредиенты не могут повторяться.")
            # ing_ids.append(ingredient['id'])
            # if not Ingredient.objects.filter(
            #     id=ingredient['id']
            # ).exists():
            #     raise ValidationError(
            #         "Ингредиента с таким id не существует.")
            # if int(ingredient['amount']) < 1:
            #     raise ValidationError(
            #         "Кол-во ингредиента не может быть меньше, чем 1.")
        # return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise ValidationError(
                "Необходимо указать тэги.")
        if len(tags) != len(set(tags)):
            raise ValidationError(
                "Тэги не могут повторяться.")
        return tags



# class RecipeSerializer(ModelSerializer):
#     # tags = TagListField(queryset=Tag.objects.all(), many=True)
#     tags = TagSerializer(many=True, read_only=True)
#     author = UserSerializer(read_only=True)
#     ingredients = IngredientInRecipeSerializer(many=True)
#     is_favorited = SerializerMethodField()
#     is_in_shopping_cart = SerializerMethodField()
#     image = Base64ImageField()

#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'tags',
#             'author',
#             'ingredients',
#             'is_favorited',
#             'is_in_shopping_cart',
#             'name',
#             'image',
#             'text',
#             'cooking_time',
#         )
#         read_only_fields = (
#             'id',
#             'author',
#             'is_favorited',
#             'is_in_shopping_cart',
#         )

#     def create(self, validated_data):
#         recipe = recipe_create_or_update(
#             self,
#             validated_data,
#             None
#         )
#         return recipe

#     def update(self, instance, validated_data):
#         update_recipe = recipe_create_or_update(
#             self,
#             validated_data,
#             instance
#         )
#         return update_recipe

#     def get_is_favorited(self, obj):
#         user = self.context['request'].user
#         return (user.is_authenticated
#                 and user.favorited.filter(recipes=obj).exists())

#     def get_is_in_shopping_cart(self, obj):
#         user = self.context['request'].user
#         return (user.is_authenticated
#                 and user.shopping_cart.filter(recipes=obj).exists())

#     def validate_ingredients(self, ingredients):
#         if not ingredients:
#             raise ValidationError(
#                 "Необходимо указать ингредиенты.")
#         ing_ids = []
#         for ingredient in ingredients:
#             if not ingredient['id'] or not ingredient['amount']:
#                 raise ValidationError(
#                     "Некорректные данные ингредиентов.")
#             if ingredient['id'] in ing_ids:
#                 raise ValidationError(
#                     "Ингредиенты не могут повторяться.")
#             ing_ids.append(ingredient['id'])
#             if not Ingredient.objects.filter(
#                 id=ingredient['id']
#             ).exists():
#                 raise ValidationError(
#                     "Ингредиента с таким id не существует.")
#             if int(ingredient['amount']) < 1:
#                 raise ValidationError(
#                     "Кол-во ингредиента не может быть меньше, чем 1.")
#         return ingredients

#     def validate_tags(self, tags):
#         if not tags:
#             raise ValidationError(
#                 "Необходимо указать тэги.")
#         if tags and len(tags) != len(set(tags)):
#             raise ValidationError(
#                 "Тэги не могут повторяться.")
#         return tags


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

    # def get_recipes_count(self, obj):
    #     return obj.recipes.count()
