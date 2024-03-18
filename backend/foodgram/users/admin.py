from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import (User, UsersSubscribes,
                     Favorited, ShoppingCart)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
    )
    list_filter = (
        'username',
        'first_name',
        'last_name',
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
  
