from api.views import (DownloadShoppingCartViewSet, FavoritedViewSet,
                       IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                       SubscribesViewSet, TagViewSet)
from django.urls import include, path
from rest_framework import routers

                        # MyUserViewSet)
                        #    MyProfileViewSet, 
                        #    ChangePasswordView)

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavoritedViewSet,
                basename='favorite')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                ShoppingCartViewSet,
                basename='shopping_cart')
# router.register(r'recipes/download_shopping_cart',
#                 DownloadShoppingCartViewSet)
router.register(r'users/(?P<id>\d+)/subscribe',
                SubscribesViewSet,
                basename='subscriptions')
router.register(r'users/subscriptions',
                SubscribesViewSet,
                basename='subscriptions')
# router.register(r'users/set_password/',
#                 ChangePasswordView,
#                 basename='set_password')
# router.register(r'users/me',
#                 MyProfileViewSet,
#                 basename='me')

urlpatterns = [
    path('', include(router.urls)),
    # path(r'^auth/', include('djoser.urls')),
    # path('users/', MyUserViewSet),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('api/', include('djoser.urls.jwt')),
    # path(r'users', include('djoser.urls')), # ?
    # path(r'auth', include('djoser.urls.jwt')), # ?
]
