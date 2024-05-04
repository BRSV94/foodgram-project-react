from django.http import HttpResponse
from django.shortcuts import render

from djoser.views import UserViewSet
from recipes.filters import RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.permissions import IsAuthorOrReadOnly
from recipes.utils import add_recipe_to, remove_recipe_from, subscribe_action
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from users.models import Favorited, ShoppingCart, UsersSubscribes
from users.utils import create_shopping_cart

from .serializers import (IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeWriteSerializer,
                          SubRecipeSerializer,
                          SubscribesSerializer,
                          TagSerializer,
                          UserSerializer)


class CustomUserViewSet(UserViewSet):

    @action(
        detail=True,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        print('LOLOLOLOKEK'*3)
        instance = request.user
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, *args, **kwargs):
        serializer = SubscribesSerializer
        obj, obj_for_action, relation_exists = subscribe_action(
            self, request, UsersSubscribes
        )

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
    
    @subscribe.mapping.delete
    def unsubscribe(self, request, *args, **kwargs):
        obj, obj_for_action, relation_exists = subscribe_action(
            self, request, UsersSubscribes
        )

        if relation_exists:
            obj.subscribes.remove(obj_for_action)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response('Вы не были подписаны на данного пользователя.',
                    status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        obj = UsersSubscribes.objects.filter(user=user).first()
        queryset = obj.subscribes.all() if obj else []
        pages = self.paginate_queryset(queryset)
        serializer = SubscribesSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        if not request.user.shopping_cart.exists():
            raise ValidationError("Ваш список покупок пуст.")

        shopping_list, filename = create_shopping_cart(request)
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, *args, **kwargs):
        return add_recipe_to(self, request, Favorited, SubRecipeSerializer)
    
    @favorite.mapping.delete
    def unfavorite(self, request, *args, **kwargs):
        return remove_recipe_from(self, request, Favorited)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, *args, **kwargs):
        return add_recipe_to(self, request, ShoppingCart, SubRecipeSerializer)
    
    @shopping_cart.mapping.delete
    def remove_with_shopping_cart(self, request, *args, **kwargs):
        return remove_recipe_from(self, request, ShoppingCart)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['^name', ]


def page_not_found(request, exception):
    return render(request, 'error_templates/404.html', status=404)
