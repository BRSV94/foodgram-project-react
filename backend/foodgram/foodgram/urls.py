"""foodgram URL Configuration"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from recipes.views import (
    RecipeViewSet, TagViewSet,
    IngredientViewSet, FavoritesViewSet,
)
from services.views import (
    SubscribtionsViewSet, ShoppingCartViewSet
)
from users.views import MyProfileViewSet, ChangePasswordView

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoritesViewSet)
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet)
router.register(r'users/subscriptions/', SubscribtionsViewSet)
router.register(r'users/set_password/', ChangePasswordView)
router.register(r'users/me/', MyProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path(r'^users/', include('djoser.urls')), # ?
    path(r'^auth/', include('djoser.urls.jwt')), # ?
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
