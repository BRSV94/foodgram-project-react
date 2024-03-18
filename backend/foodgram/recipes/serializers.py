# import base64
# import webcolors
# from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
#                                         PrimaryKeyRelatedField,
#                                         ImageField, Field, ValidationError,)
# from rest_framework.exceptions import ValidationError
# from django.shortcuts import get_object_or_404
# from .models import Recipe, Tag, Ingredient, IngredientInRecipe
# from users.models import User
# from users import serializers
# from django.core.files.base import ContentFile


# class Base64ImageField(ImageField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]

#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#         return super().to_internal_value(data)
    

# class Hex2NameColor(Field):
#     def to_representation(self, value):
#         return value

#     def to_internal_value(self, data):
#         try:
#             data = webcolors.hex_to_name(data)
#         except ValueError:
#             raise ValidationError('Для этого цвета нет имени')
#         return data



# class TagSerializer(ModelSerializer):

#     color = Hex2NameColor()
    
#     class Meta:
#         model = Tag
#         fields = ('id', 'name', 'color', 'slug',)
#         read_only_fields = ('id', 'name', 'color', 'slug',)


# class IngredientSerializer(ModelSerializer):
    
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit',)
#         read_only_fields = ('id', 'name', 'measurement_unit',)


# class IngredientInRecipeSerializer(ModelSerializer):
#     name = SerializerMethodField()
#     measurement_unit = SerializerMethodField()

#     def get_name(self, obj):
#         return obj.ingredients.first().name
    
#     def get_measurement_unit(self, obj):
#         return obj.ingredients.first().measurement_unit

#     class Meta:
#         model = IngredientInRecipe
#         fields = ('id', 'name', 'measurement_unit', 'amount',)


# class RecipeGetSerializer(ModelSerializer):
#     tags = TagSerializer(many=True, read_only=True)
#     author = serializers.UserSerializer(read_only=True)
#     ingredients = IngredientInRecipeSerializer(many=True, read_only=True)
#     is_favorited = SerializerMethodField()
#     is_in_shopping_cart = SerializerMethodField()
#     image = Base64ImageField(required=False, allow_null=True)


#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
#                   'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',)
#         read_only_fields = ('id', 'author', 'is_favorited', 'is_in_shopping_cart',)


#     def get_is_favorited(self, obj):
#         user = self.context['request'].user
#         return (user.is_authenticated and
#                 user.favorited.filter(recipes=obj).exists())
    
#     def get_is_in_shopping_cart(self, obj):
#         user = self.context['request'].user
#         return (user.is_authenticated and
#                 user.shopping_cart.filter(recipes=obj).exists())





# # class RecipeGetSerializer(ModelSerializer):
# #     tags = TagSerializer(many=True)
# #     Ingredient = IngredientSerializer(many=True)
# #     is_favorited = SerializerMethodField()
# #     is_in_shopping_cart = SerializerMethodField()

# #     class Meta:
# #         model = Recipe
# #         fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
# #                   'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',)
# #         read_only_fields = ('id', 'author', 'is_favorited', 'is_in_shopping_cart',)

# #     def get_is_favorited(self, obj):
# #         user = self.context['request'].user
# #         return (user.is_authenticated and
# #                 user.favorited.filter(recipes=obj).exists())
    
# #     def get_is_in_shopping_cart(self, obj):
# #         user = self.context['request'].user
# #         return (user.is_authenticated and
# #                 user.shopping_cart.filter(recipes=obj).exists())
    

# class RecipePostSerializer(ModelSerializer):

#     tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True) #???
#     image = Base64ImageField(required=False, allow_null=True)
#     ingredients = IngredientSerializer(many=True)
#     author = serializers.UserSerializer()
    
#     class Meta:
#         model = Recipe
#         fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',)

#     def validate_ingredients(self, attrs) -> list[tuple]:
#         ingredients = attrs
#         valided_ingredients = []
#         for ingredient in ingredients:
#             amount = ingredient['amount']
#             if amount > 0:
#                 valided_ingredient = get_object_or_404(Ingredient, id=ingredient['id'])
#                 valided_ingredients.append((valided_ingredient, amount))
#             raise ValidationError({'amount': 'Значение должно быть положительным.'})

#         return valided_ingredients

#     def validate_tags(self, attrs):
#         tags = attrs
#         if tags:
#             if len(tags) == len(set(tags)):
#                 valided_tags = []
#                 for tag_id in tags:
#                     valided_tags.append(get_object_or_404(Tag, id=tag_id))
#                 return valided_tags
            
#             raise ValidationError(
#                 {'tags': 'Тэги не должны повторяться.'})

#         raise ValidationError(
#             {'tags': 'Нужно указать не менее одного тэга.'})
        
#     def create(self, validated_data):

#         author = self.context.get('request').user
#         validated_data['author'] = author
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         recipe = Recipe.objects.create(**validated_data)

#         for ingredient in ingredients:
#             ing = ingredient[0]
#             amount = ingredient[1]
#             obj = IngredientInRecipe.objects.create(
#                 recipe=recipe,
#                 ingredient=ing,
#                 amount=amount,
#             )
#         for tag in tags:
#             recipe.tags.add(tag)

#         return recipe
