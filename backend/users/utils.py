from aspose import pdf
from django.shortcuts import get_object_or_404

from .models import ShoppingCart


def create_shopping_cart(request):

    user = request.user
    cart = get_object_or_404(ShoppingCart, user=user)
    recipes = cart.recipes.all()

    ingredients = dict()
    for recipe in recipes:
        for ing_obj in recipe.ingredients.all():
            ingredient = str(ing_obj.ingredient)
        ingredients[ingredient] = ingredients.get(
            ingredient,
            0
        ) + ing_obj.amount

    body_text = ''
    for ingr, amount in ingredients.items():
        body_text += f'{ingr} - {amount}\n'
    file = ('Cписок покупок пользователя '
            f'{user.first_name, user.last_name}:\n\n'
            + body_text)
    file_name = f'список_покупок_{user.username}'
    return (file, file_name)
