from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Favorited, ShoppingCart, User, UsersSubscribes

from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .utils import create_shopping_cart

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    def download_shopping_cart(self, request, queryset):
        user = request.user
        if not user.shopping_cart.exists():
            raise ValidationError("Ваш список покупок пуст.")
        shopping_list_pdf, pdf_name = create_shopping_cart(request)
        response = HttpResponse(shopping_list_pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={pdf_name}'
        return response

    download_shopping_cart.short_description = "Download Shopping Cart PDF"


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'username',
        'first_name',
        'last_name',
        'email',
    )


@admin.register(UsersSubscribes)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )
    list_filter = (
        'user',
        'subscribes',
    )
    filter_horizontal = (
        'subscribes',
    )
        

@admin.register(Favorited)
class FavoritedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )
    list_filter = (
        'user',
        'recipes',
    )
    filter_horizontal = (
        'recipes',
    )


@admin.register(ShoppingCart)
class ShoppingCartdAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )
    list_filter = (
        'user',
        'recipes',
    )
    filter_horizontal = (
        'recipes',
    )
  
