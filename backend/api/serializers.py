import base64

import webcolors
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from recipes.models import (
    Ingredient, IngredientInRecipe,
    Recipe, Tag,
)
from recipes.utils import recipe_bind_ingredients_and_tags
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField, Field, ImageField, IntegerField,
    ModelSerializer, PrimaryKeyRelatedField,
    SerializerMethodField, ValidationError,
)
from users.models import User, UsersSubscribes


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

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('id',)

class UserCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
        read_only_fields = ('id', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}}



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


# class IngredientInRecipeSerializer(ModelSerializer):
#     name = SerializerMethodField()
#     measurement_unit = SerializerMethodField()

#     def get_name(self, obj):
#         return obj.ingredient.name
    
#     def get_measurement_unit(self, obj):
#         return obj.ingredient.measurement_unit.measurement_unit
    
#     def create(self, validated_data):
#         print(validated_data)
    

    # class Meta:
    #     model = IngredientInRecipe
    #     fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientInRecipeSerializer(ModelSerializer):
    id = IntegerField(
        # write_only=True
        )
    amount = IntegerField(
        # write_only=True,
        min_value=1,
    )
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()

    def get_name(self, obj):
        return obj.ingredient.name
    
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit.measurement_unit
    
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount') #
        read_only_fields = ('name', 'measurement_unit',) #

    # def to_representation(self, instance):
    #     print(instance, "LOLOKEKE")
    #     return super().to_representation(instance)


class TagListField(PrimaryKeyRelatedField):
    def to_representation(self, value):
        return {'id': value.id, 'name': value.name,
                'color': value.color, 'slug': value.slug}


class RecipeSerializer(ModelSerializer):
    tags = TagListField(queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True,
        # read_only=True,
        # source='ingredient_in_recipe'
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',)
        read_only_fields = ('id', 'author', 'is_favorited', 'is_in_shopping_cart',)

    def create(self, validated_data):
        recipe = recipe_bind_ingredients_and_tags(
            self,
            validated_data,
            None
        )
        # ingredients_data = validated_data.pop('ingredients')
        # tags_data = validated_data.pop('tags')
        # recipe = Recipe.objects.create(**validated_data)

        # for ingredient_data in ingredients_data:
        #     ing_id = ingredient_data['id']
        #     ing_amount = ingredient_data['amount']
        #     ingredient = Ingredient.objects.get(id=ing_id)
        #     ing_in_recipe = IngredientInRecipe.objects.create(
        #     #     recipe=recipe,
        #         ingredient=ingredient,
        #         amount=ing_amount,
        #     )
        #     recipe.ingredients.add(ing_in_recipe)

        # recipe.tags.set(tags_data)
        return recipe
    
    def update(self, instance, validated_data):
        update_recipe =  recipe_bind_ingredients_and_tags(
            self,
            validated_data,
            instance
        )
        return update_recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated and
                user.favorited.filter(recipes=obj).exists())
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated and
                user.shopping_cart.filter(recipes=obj).exists())

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise ValidationError(
                    "Необходимо указать ингредиенты.")
        ing_ids = []
        for ingredient in ingredients:
            if not ingredient['id'] or not ingredient['amount']:
                raise ValidationError(
                    "Некорректные данные ингредиентов.")
            if ingredient['id'] in ing_ids:
                raise ValidationError(
                    "Ингредиенты не могут повторяться.")
            ing_ids.append(ingredient['id'])
            if not Ingredient.objects.filter(
                id=ingredient['id']
            ).exists():
                raise ValidationError(
                    "Ингредиента с таким id не существует.")
            if int(ingredient['amount']) < 1:
                raise ValidationError(
                    "Кол-во ингредиента не может быть меньше, чем 1.")
        return ingredients


    def validate_tags(self, tags):
        if not tags:
            raise ValidationError(
                "Необходимо указать тэги.")
        if tags and len(tags) != len(set(tags)):
            raise ValidationError(
                "Тэги не могут повторяться.")
        return tags
        
    # def validate_image(self, image):
    #     if not image:
    #         raise ValidationError(
    #             "Необходимо загрузить изображение.")
    #     return image

    # Сверху было image = Base64ImageField(required=False, allow_null=True)



# class FavoritedSerializer(ModelSerializer):

#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time',)
#         read_only_fields = ('id', 'name', 'image', 'cooking_time',)


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)
        if request:
            limit = request.query_params.get('recipes_limit', None)
            if limit:
                data['recipes'] = data['recipes'][:int(limit)]
        
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
