# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
# from rest_framework import filters, status, viewsets, mixins, permissions
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Tag, Ingredient, Recipe
# from users.models import Favorited, UsersSubscribes, User
# from users.permissions import IsOwnerProfile
# from api.serializers import (RecipeGetSerializer, RecipePostSerializer,
#                           IngredientSerializer,
#                           SubscribesSerializer, TagSerializer)
# from .filters import RecipeFilter
# from django.shortcuts import get_object_or_404

# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     # serializer_class = RecipeSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = RecipeFilter
#     permission_classes = (IsAuthenticatedOrReadOnly,)


#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return RecipeGetSerializer
#         return RecipePostSerializer


#     # def perform_create(self, serializer):
#     #     serializer.save(author=self.request.user)


# class TagViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer


# class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer


# class SubscribesViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
#                         mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = UsersSubscribes.objects.all()
#     serializer_class = SubscribesSerializer
#     permission_classes = (IsOwnerProfile,)

#     def get_queryset(self):
#         user_id = self.request.user.id
#         subscribes = get_object_or_404(UsersSubscribes, id=user_id)
#         queryset = subscribes.subscribes.all()
#         return queryset

#     # def create(self, request, *args, **kwargs):
#     #     subscribe_id = self.kwargs.get('id')
#     #     get_object_or_404(User, id=subscribe_id)
#     #     # Непонятка с редоком. Зачем передавать в теле запроса все данные пользователя? 
#     #     user = UsersSubscribes.objects.get_or_create(user=request.user)

#     #     if user.subscribes.filter(id=subscribe_id).exists():
#     #         return Response("Вы уже подписаны на пользователя.", status=status.HTTP_400_BAD_REQUEST)
        
#     #     # serializer = self.get_serializer(data=request.data)
#     #     # serializer.is_valid(raise_exception=True)
#     #     user.subscribes.create(id=subscribe_id)
#     #     headers = self.get_success_headers(serializer.data)
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
