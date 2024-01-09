from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters, status, viewsets, mixins, permissions
from .mixin import BaseRecipeMixin
from models import Tag, Ingredient, Recipe
from users.models import Favorites
from .serializers import (RecipeSerializer, TagSerializer,
                          IngredientSerializer, FavoritesSerializer,)

class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = () # Finish it.
    serializer_class = RecipeSerializer

    def get_queryset(self):
        if self.request.data['is_favorited']:
            return Recipe.objects.filter() #annotate?
        return Recipe.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TagViewSet(BaseRecipeMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class FavoritesViewSet(BaseRecipeMixin, mixins.ListModelMixin):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
