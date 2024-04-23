from django.http import HttpResponse
from djoser.views import UserViewSet
from recipes.filters import RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.permissions import IsAuthorOrReadOnly
from django.shortcuts import render
from recipes.utils import recipe_action, subscribe_action
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from users.models import Favorited, ShoppingCart, UsersSubscribes
from users.utils import create_shopping_cart

from .serializers import (
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            raise ValidationError("Ваш список покупок пуст.")

        shopping_list_pdf, pdf_name = create_shopping_cart(request)
        response = HttpResponse(
            shopping_list_pdf,
            content_type='application/pdf'
        )
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

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, *args, **kwargs):
        model = ShoppingCart
        serializer = SubRecipeSerializer
        return recipe_action(self, request, model, serializer)
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            raise ValidationError("Ваш список покупок пуст.")

        shopping_list_pdf, pdf_name = create_shopping_cart(request)
        response = HttpResponse(
            shopping_list_pdf,
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename={pdf_name}'
        return response


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
