from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import Recipe
from users.models import User


def preparation(self, request, submodel, obj_for_action):

    relation_exists = submodel.objects.filter(
        user=request.user,
        recipes=obj_for_action
    ).exists()

    obj, create = submodel.objects.get_or_create(user=request.user)
    return obj, obj_for_action, relation_exists


def add_recipe_to(self, request, submodel, serializer):
    EXISTS_MESSAGES = {
        'Favorited': 'Рецепт  уже в избранном.',
        'ShoppingCart': 'Рецепт уже в списке покупок.',
    }

    try:
        obj_for_add_id = self.kwargs.get('pk')
        obj_for_add = Recipe.objects.get(id=obj_for_add_id)
        obj, obj_for_add, relation_exists = preparation(
            self, request, submodel, obj_for_add)

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

    except ObjectDoesNotExist:
        raise ValidationError('Рецепта с таким id не существует.')


def remove_recipe_from(self, request, submodel):
    NO_EXISTS_MESSAGES = {
        'Favorited': 'Рецепт не был в избранном.',
        'ShoppingCart': 'Рецепт не был в списке покупок.',
    }

    obj_for_action_id = self.kwargs.get('pk')
    obj_for_remove = get_object_or_404(Recipe, id=obj_for_action_id)

    obj, obj_for_remove, relation_exists = preparation(
        self, request, submodel, obj_for_remove)

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
