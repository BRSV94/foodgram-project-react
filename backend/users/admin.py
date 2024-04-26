from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Favorited, ShoppingCart, User, UsersSubscribes


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'subscribes_count'
        'email',
    )
    list_filter = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    @admin.display(description='кол-во подписчиков')
    def subscribes_count(self, obj):
        print(obj.subscriber.subscribes.all())
        # print(obj.subscriber.subscribes.count())
        return obj.subscriber.subscribes.all()


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
