# from django.shortcuts import get_object_or_404
# from rest_framework import viewsets, mixins, status, generics
# from rest_framework.response import Response
# from .models import User, Favorited
# from recipes.models import Recipe
# from .serializers import (UserSerializer, ChangePasswordSerializer,
#                           FavoritedSerializer)
# from .permissions import IsOwnerProfile


# class MyProfileViewSet(viewsets.GenericViewSet):

#     def retrieve(self, request, *args, **kwargs):
#         instance = User.objects.get(pk=self.request.user.pk)
#         serializer = UserSerializer(instance)
#         return Response(serializer.data)


# class ChangePasswordView(generics.UpdateAPIView):
#         serializer_class = ChangePasswordSerializer
#         model = User
#         permission_classes = (IsOwnerProfile,)

#         def get_object(self, queryset=None):
#             obj = self.request.user
#             return obj

#         def update(self, request, *args, **kwargs):
#             self.object = self.get_object()
#             serializer = self.get_serializer(data=request.data)

#             if serializer.is_valid():
#                 if self.object.check_password(serializer.data.get("current_password")):
#                     self.object.set_password(serializer.data.get("new_password"))
#                     self.object.save()
#                     return Response(status=status.HTTP_204_NO_CONTENT)

#             return Response(status=status.HTTP_400_BAD_REQUEST)


# class FavoritedViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
#                        viewsets.GenericViewSet):
#     serializer_class = FavoritedSerializer
#     permission_classes = (IsOwnerProfile,)

#     def destroy(self, request, *args, **kwargs):
#         recipe_id = self.kwargs.get('recipe_id')
#         recipe = Recipe.objects.get(id=recipe_id)
#         user = request.user
#         if Favorited.objects.filter(user=user).exists():
#             obj = Favorited.objects.get(user=user)
#             if recipe in obj.recipes:
#                 obj.recipes.remove(recipe)

#             return Response(status=status.HTTP_204_NO_CONTENT)
        
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     # Будет работать "in" с QuerySet?


#     # def perform_create(self, serializer):
#     #     serializer.save(user=self.request.user)

#     # def get_queryset(self):
#     #     user = self.request.user
#     #     queryset = Recipe.favorite_in.filter(author=user)
#     #     return queryset
