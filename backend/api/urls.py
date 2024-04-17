from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    # SubscribeViewSet,
    CustomUserViewSet,
)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
# router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
#                 FavoritedViewSet,
                # basename='favorite')
# router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
#                 ShoppingCartViewSet,
#                 basename='shopping_cart')
# router.register(r'users/(?P<id>\d+)/subscribe',
#                 SubscribesViewSet,
#                 basename='subscriptions')
router.register(r'users',
                CustomUserViewSet,
                basename='users')
# router.register(r'users/subscriptions',
#                 SubscribeViewSet,
#                 basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
