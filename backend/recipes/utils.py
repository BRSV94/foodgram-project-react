import inspect

from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from rest_framework import status
from rest_framework.response import Response
from users.models import User


def preparation(self, request, submodel):
    print('LOL1')
    obj_for_action_id = self.kwargs.get('pk')
    print('LOL2')
    try:
        print('LOL3')
        obj_for_action = Recipe.objects.filter(
            id=obj_for_action_id
        ).first()
        print('LOL4')

        relation_exists = submodel.objects.filter(
            user=request.user,
            recipes=obj_for_action
        ).exists()
        print('LOL5')

        obj, create = submodel.objects.get_or_create(user=request.user)
        print('LOL7')
        return obj, obj_for_action, relation_exists

    except:
        raise ValidationError('Рецепта с таким id не существует.')


def add_to_recipe(self, request, submodel, serializer):
    EXISTS_MESSAGES = {
        'Favorited':  'Рецепт  уже в избранном.',
        'ShoppingCart': 'Рецепт уже в списке покупок.',
    }
    print("It's OK")
    obj, obj_for_add, relation_exists = preparation(self, request, submodel)
    print('No fucking shit.')

    if not relation_exists:
        obj.recipes.add(obj_for_add)
        data = serializer(instance=obj_for_add).data
        serializer = serializer(instance=obj_for_add, data=data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    return Response(EXISTS_MESSAGES[submodel.__name__],
                        status=status.HTTP_400_BAD_REQUEST)


def remove_from_recipe(self, request, submodel):
    NO_EXISTS_MESSAGES = {
        'Favorited': 'Рецепт не был в избранном.',
        'ShoppingCart': 'Рецепт не был в списке покупок.',
    }

    obj, obj_for_remove, relation_exists = preparation(self, request, submodel)

    if relation_exists:
        obj.recipes.remove(obj_for_remove)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(NO_EXISTS_MESSAGES[submodel.__name__],
                        status=status.HTTP_400_BAD_REQUEST)


def subscribe_action(self, request, submodel):
    obj_for_action_id = self.kwargs.get('id')
    if int(obj_for_action_id) == request.user.id:
        raise ValidationError('Нельзя подписаться на себя.')

    obj_for_action = get_object_or_404(User, id=obj_for_action_id)
    relation_exists = submodel.objects.filter(
        user=request.user,
        subscribes=obj_for_action
    ).exists()

    obj, create = submodel.objects.get_or_create(user=request.user)
    return obj, obj_for_action, relation_exists
    # if request.method == 'POST':
    #     if not relation_exists:
    #         obj.subscribes.add(obj_for_action)
    #         data = serializer(instance=obj_for_action).data
    #         serializer = serializer(
    #             instance=obj_for_action,
    #             data=data)
    #         serializer.is_valid(raise_exception=False)
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED,
    #         )

    #     return Response('Вы уже подписаны на данного пользователя.',
    #                     status=status.HTTP_400_BAD_REQUEST)

    # if relation_exists:
    #     obj.subscribes.remove(obj_for_action)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # return Response('Вы не были подписаны на данного пользователя.',
    #                 status=status.HTTP_400_BAD_REQUEST)


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
            ingredient_id=ing_id,
            amount=ing_amount,
        ))
    ingredients_objs = IngredientInRecipe.objects.bulk_create(ingredients)
    recipe.ingredients.set(ingredients_objs)
    recipe.tags.set(tags_data)
    return recipe
