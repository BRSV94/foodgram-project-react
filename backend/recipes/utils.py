import inspect

from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, IngredientInRecipe, Recipe
from rest_framework import status
from rest_framework.response import Response
from users.models import User


def add(self, serializer, obj, obj_for_add):
    obj.recipes.add(obj_for_add)
    data = serializer(instance=obj_for_add).data
    serializer = serializer(instance=obj_for_add, data=data)
    serializer.is_valid(raise_exception=False)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers)


def remove(obj, obj_for_remove):
    obj.recipes.remove(obj_for_remove)
    return Response(status=status.HTTP_204_NO_CONTENT)


def recipe_action(self, request, submodel, serializer):
    MESSAGE_LIST = {
        'favorite': {
            'exists_message': 'Рецепт  уже в избранном.',
            'no_exists_message': 'Рецепт не находился в избранном.'
        },
        'shopping_cart': {
            'exists_message': 'Рецепт уже в списке покупок.',
            'no_exists_message': 'Рецепт не был в списке покупок.'
        }
    }

    call_func_name = inspect.currentframe().f_back.f_code.co_name
    obj_for_action_id = self.kwargs.get('pk')
    if request.method == 'delete':
        obj_for_action = get_object_or_404(Recipe, id=obj_for_action_id)
    else:
        if not Recipe.objects.filter(id=obj_for_action_id).exists():
            return Response('Рецепта с таким id не существует.',
                            status=status.HTTP_400_BAD_REQUEST)
        obj_for_action = Recipe.objects.get(id=obj_for_action_id)

    relation_exists = submodel.objects.filter(
        user=request.user,
        recipes=obj_for_action
    ).exists()

    obj, create = submodel.objects.get_or_create(user=request.user)
    serializer = serializer
    if request.method == 'POST':
        if not relation_exists:
            return add(self, serializer, obj, obj_for_action)

        return Response(MESSAGE_LIST[call_func_name]['exists_message'],
                        status=status.HTTP_400_BAD_REQUEST)

    if relation_exists:
        return remove(obj, obj_for_action)

    return Response(MESSAGE_LIST[call_func_name]['no_exists_message'],
                    status=status.HTTP_400_BAD_REQUEST)


def subscribe_action(self, request, submodel, serializer):
    obj_for_action_id = self.kwargs.get('id')
    if int(obj_for_action_id) == request.user.id:
        return Response('Нельзя подписаться на себя.',
                        status=status.HTTP_400_BAD_REQUEST)

    obj_for_action = get_object_or_404(User, id=obj_for_action_id)
    relation_exists = submodel.objects.filter(
        user=request.user,
        subscribes=obj_for_action
    ).exists()

    obj, create = submodel.objects.get_or_create(user=request.user)
    serializer = serializer
    if request.method == 'POST':
        if not relation_exists:
            obj.subscribes.add(obj_for_action)
            data = serializer(instance=obj_for_action).data
            serializer = serializer(
                instance=obj_for_action,
                data=data)
            serializer.is_valid(raise_exception=False)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response('Вы уже подписаны на данного пользователя.',
                        status=status.HTTP_400_BAD_REQUEST)

    if relation_exists:
        obj.subscribes.remove(obj_for_action)
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response('Вы не были подписаны на данного пользователя.',
                    status=status.HTTP_400_BAD_REQUEST)


def recipe_create_or_update(self, validated_data, recipe):
    ingredients_data = validated_data.pop('ingredients')
    tags_data = validated_data.pop('tags')
    if not recipe:
        recipe = Recipe.objects.create(**validated_data)
    for ingredient_data in ingredients_data:
        ing_id = ingredient_data['id']
        ing_amount = ingredient_data['amount']
        ingredient = Ingredient.objects.get(id=ing_id)
        ing_in_recipe, create = IngredientInRecipe.objects.get_or_create(
            ingredient=ingredient,
            amount=ing_amount,
        )
        recipe.ingredients.add(ing_in_recipe)
    recipe.tags.set(tags_data)
    return recipe
