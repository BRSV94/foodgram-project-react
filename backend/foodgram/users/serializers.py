# from rest_framework import serializers
# from users.models import User, Favorited, UsersSubscribes
# from recipes.models import Recipe
# from recipes.serializers import RecipeGetSerializer
# from django.shortcuts import get_object_or_404

# class UserSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     def get_is_subscribed(self, obj):
#         user = obj
#         current_user = self.context.get('request').user
#         return UsersSubscribes.objects.filter(
#             user=current_user, subcribes=user).exists()

#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name',
#                   'last_name', 'is_subscribed',)
#         read_only_fields = ('id', 'is_subscribed',)


# class ChangePasswordSerializer(serializers.Serializer):
#     model = User

#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

    
# class FavoritedSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time',)
#         read_only_fields = ('id', 'name', 'image', 'cooking_time',)

#     def create(self, validated_data):
#         user = self.context.get('request').user
#         recipe_id = self.context.get('view').kwargs.get('recipe_id') # View?
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         obj, create = Favorited.objects.get_or_create(user=user)
#         obj.recipes.add(recipe)
#         return recipe




# class SubscribesSerializer(serializers.ModelSerializer):
#     # is_subscribed = SerializerMethodField()
#     recipes = serializers.SerializerMethodField()
#     recipes_count = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name',
#                   'last_name', 'is_subscribed', 'recipes',
#                   'recipes_count',)

#     # def get_is_subscribed(self, obj):

#     def get_recipes(self, obj):
#         limit = self.context['request'].GET.get('recipes_limit')
#         recipes = obj.recipes.all()
#         if limit and limit.isdigit():
#             recipe = recipe[:int(limit)]
#         serializer = RecipeGetSerializer(recipes, many=True, read_only=True)
#         return serializer.data

#     def get_recipes_count(self, obj):
#         return obj.recipes.count()



