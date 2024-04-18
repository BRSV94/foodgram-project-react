from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.filters import RecipeFilter
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from recipes.permissions import IsAuthorOrReadOnly
from recipes.utils import recipe_action, subscribe_action
from recipes.validators import (image_validator,
                                ingredients_validator,
                                tags_validator)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from users.models import Favorited, ShoppingCart, User, UsersSubscribes
from users.permissions import IsOwnerProfile
from users.utils import create_shopping_cart

from .serializers import (
    IngredientInRecipeSerializer,
    IngredientSerializer, RecipeSerializer,
    SubRecipeSerializer, SubscribesSerializer,
    TagSerializer,
)

class CustomUserViewSet(UserViewSet):

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, *args, **kwargs):
        model = UsersSubscribes
        serializer = SubscribesSerializer
        return subscribe_action(self, request, model, serializer)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        # queryset = User.objects.filter(subscriber__user=user)
        obj, create = UsersSubscribes.objects.get_or_create(
            user=user
        )
        queryset = obj.subscribes.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscribesSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     return super().create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     '''
    #     Извлекаем данные об ингредиентах до валидации.
    #     Валидируем остальные данные.
    #     Создаем рецепт в бд.
    #     Добавляем ингредиенты в нужном виде в рецепт.
    #     Выводим данные ингредиентов в нужном виде.
    #     '''
    #     serializer = self.get_serializer(data=request.data)
    #     # ingredients = serializer.initial_data.pop('ingredients', None)
    #     # ingredients_validator(self, ingredients) #
    #     # tags = serializer.initial_data.get('tags', None)
    #     # tags_validator(self, tags)
    #     # image = serializer.initial_data.get('image', None)
    #     # image_validator(self, image)

    #     # if not ingredients:
    #     #     return Response("Необходимо указать ингредиенты.",
    #     #                     status=status.HTTP_400_BAD_REQUEST)
    #     # ing_ids = []
    #     # for ingredient in ingredients:
    #     #     if ingredient['id'] in ing_ids:
    #     #         return Response("Ингредиенты не могут повторяться.",
    #     #                     status=status.HTTP_400_BAD_REQUEST)
    #     #     ing_ids.append(ingredient['id'])
    #     # ing_ids.clear()
        
    #     # tags = serializer.initial_data.get('tags', None)
    #     # if not tags:
    #     #     return Response("Необходимо указать тэги.",
    #     #                     status=status.HTTP_400_BAD_REQUEST)
    #     # if tags and len(tags) != len(set(tags)):
    #     #     return Response("Тэги не могут повторяться.",
    #     #                     status=status.HTTP_400_BAD_REQUEST)
        
    #     ingredients = serializer.initial_data.pop('ingredients', None)
    #     ingredients_validator(self, ingredients)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     serializer.data['ingredients'] = []
    #     recipe = Recipe.objects.get(id=serializer.data['id'])
    #     # if ingredients:
        
    #     for ingredient_data in ingredients:
    #         ing_exists = Ingredient.objects.filter(id=ingredient_data['id']).exists()
    #         if not ing_exists:
    #             recipe.delete()
    #             break
    #         ingredient = Ingredient.objects.get(id=ingredient_data['id'])
    #         if int(ingredient_data['amount']) < 1:
    #             recipe.delete()
    #             raise ValidationError(
    #                 "Кол-во ингредиента не может быть меньше 1.")
    #         saved_ingredient = IngredientInRecipe.objects.create(
    #             recipe=recipe,
    #             ingredient=ingredient,
    #             amount=ingredient_data['amount']
    #         )
    #         to_ingredients = IngredientInRecipeSerializer(instance=saved_ingredient).data
    #         serializer.data['ingredients'].append(to_ingredients)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
    #     raise ValidationError("Указан id несуществующего ингредиента.")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            raise ValidationError("Ваш список покупок пуст.")

        shopping_list_pdf, pdf_name = create_shopping_cart(request)
        response = HttpResponse(shopping_list_pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={pdf_name}'
        return response

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, *args, **kwargs):
        model = Favorited
        serializer = SubRecipeSerializer
        return recipe_action(self, request, model, serializer)

    @action(detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, *args, **kwargs):
        model = ShoppingCart
        serializer = SubRecipeSerializer
        return recipe_action(self, request, model, serializer)
        

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['^name',]
