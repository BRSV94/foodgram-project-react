from rest_framework.response import Response
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated)
from rest_framework import (filters, status, viewsets,
                            mixins, permissions, generics)
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe
from users.models import User, Favorited, UsersSubscribes, ShoppingCart
from users.permissions import IsOwnerProfile
from .serializers import (RecipeSerializer, TagSerializer, SubRecipeSerializer,
                          IngredientSerializer, SubscribesSerializer,
                          FavoritedSerializer, IngredientInRecipeSerializer)
                        #   ChangePasswordSerializer,
                        #   UserSerializer,
from recipes.filters import RecipeFilter, IngredientFilter
from recipes.permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request, *args, **kwargs):
        '''
        Извлекаем данные об ингредиентах до валидации.
        Валидируем остальные данные.
        Создаем рецепт в бд.
        Добавляем ингредиенты в нужном виде в рецепт.
        Выводим данные ингредиентов в нужном виде.
        '''
        serializer = self.get_serializer(data=request.data)
        ingredients = serializer.initial_data.pop('ingredients', None)
        if not ingredients:
            return Response("Необходимо указать ингредиенты.",
                            status=status.HTTP_400_BAD_REQUEST)
        tags = serializer.initial_data.get('tags', None)
        if tags and len(tags) != len(set(tags)):
            return Response("Тэги не могут повторяться.",
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.data['ingredients'] = []
        recipe = Recipe.objects.get(id=serializer.data['id'])

        for ingredient_data in ingredients:
            try:
                ingredient = Ingredient.objects.get(id=ingredient_data['id'])
                if ingredient_data['amount'] < 1:
                    return Response("Кол-во ингредиента не может быть меньше 1.",
                                    status=status.HTTP_400_BAD_REQUEST)
                saved_ingredient = IngredientInRecipe.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=ingredient_data['amount']
                )
                to_ingredients = IngredientInRecipeSerializer(instance=saved_ingredient).data
                serializer.data['ingredients'].append(to_ingredients)
            except:
                    return Response("Некорректные данные ингредиентов или тэгов.",
                                    status=status.HTTP_400_BAD_REQUEST)
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def validate_amount(value):
    #     return value > 0
    
    # def update(self, request, *args, **kwargs):
    #     recipe_id = self.kwargs.get('recipe_id')

    #     return super().update(request, *args, **kwargs)


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


class SubscribesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = SubscribesSerializer
    permission_classes = (IsOwnerProfile,)
    # pagination_class = SubscribesPagination

    def get_queryset(self):
        current_user = self.request.user
        if self.request.method == 'GET':
            '''
            Вернуть пользователей, на который текущий юзер подписан.
            '''
            subscribe_obj, create = UsersSubscribes.objects.get_or_create(user=current_user)
            queryset = subscribe_obj.subscribes.all()
            return queryset
        else:
            '''
            Вернуть объект модели подписки.
            '''
            queryset = UsersSubscribes.objects.filter(user=current_user)
        
    def create(self, request, *args, **kwargs):
        subscribe_id = self.kwargs.get('id')
        user_for_subscribe = get_object_or_404(User, id=subscribe_id)
        obj, create = UsersSubscribes.objects.get_or_create(user=request.user)

        if int(subscribe_id) == request.user.id:
            return Response(f'Нельзя подписаться на себя.',
                            status=status.HTTP_400_BAD_REQUEST)

        if UsersSubscribes.objects.filter(
            user=request.user,
            subscribes=user_for_subscribe
        ).exists():
            return Response(f'Вы уже подписаны на {user_for_subscribe}.',
                            status=status.HTTP_400_BAD_REQUEST)
        # query_params = self.request.query_params

        obj.subscribes.add(user_for_subscribe)
        data = SubscribesSerializer(instance=user_for_subscribe).data

        if request.query_params:
            recipes_limit = int(self.request.query_params['recipes_limit'])
            data['recipes'] = data['recipes'][:recipes_limit]
        # print(data)

        # serializer = SubscribesSerializer(instance=user_for_subscribe, data=data)
        # serializer.is_valid(raise_exception=True)
        # print('LOSOSOSOSOSOS')
        # print(serializer.data)
        headers = self.get_success_headers(data)
            # serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        unsubscribe_id = self.kwargs.get('id')
        user_for_unsubscribe = get_object_or_404(User, id=unsubscribe_id)

        if not UsersSubscribes.objects.filter(
            user=request.user,
            subscribes=user_for_unsubscribe
        ).exists():
            return Response(f'Вы не были подписаны на {user_for_unsubscribe}.',
                            status=status.HTTP_400_BAD_REQUEST)

        obj = UsersSubscribes.objects.get(user=request.user)
        obj.subscribes.remove(user_for_unsubscribe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoritedViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = FavoritedSerializer
    permission_classes = (IsOwnerProfile,)

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe_for_favorite = get_object_or_404(Recipe, id=recipe_id)

        if Favorited.objects.filter(
                user=request.user,
                recipes=recipe_for_favorite
        ).exists():
            return Response(f'Рецепт "{recipe_for_favorite}" уже в избранном.',
                            status=status.HTTP_400_BAD_REQUEST)

        obj, create = Favorited.objects.get_or_create(user=request.user)
        obj.recipes.add(recipe_for_favorite)
        data = FavoritedSerializer(instance=recipe_for_favorite).data
        serializer = FavoritedSerializer(instance=recipe_for_favorite, data=data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        remove_recipe_id = self.kwargs.get('recipe_id')
        remove_recipe = get_object_or_404(Recipe, id=remove_recipe_id)

        if not Favorited.objects.filter(
            user=request.user,
            recipes=remove_recipe
        ).exists():
            return Response('Рецепт не находится в избраноом.',
                            status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubRecipeSerializer

    def create(self, request, *args, **kwargs):
        cart, create = ShoppingCart.objects.get_or_create(user=request.user)
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if ShoppingCart.objects.filter(
            user=request.user,
            recipes=recipe
        ).exists():
            return Response('Данный рецепт уже в списке покупок.',
                            status=status.HTTP_400_BAD_REQUEST)

        data = SubRecipeSerializer(instance=recipe).data
        serializer = self.get_serializer(data=data)
        print(serializer.initial_data)
        headers = self.get_success_headers(serializer.initial_data)

        cart.recipes.add(recipe)
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        cart, create = ShoppingCart.objects.get_or_create(user=request.user)
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if not ShoppingCart.objects.filter(
            user=request.user, recipes=recipe
        ).exists():
            return Response('Данный рецепта нет в списке покупок.',
                            status=status.HTTP_400_BAD_REQUEST)

        cart.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartViewSet(viewsets.ViewSetMixin):
    pass
