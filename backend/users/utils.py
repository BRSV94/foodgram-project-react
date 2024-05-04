from django.shortcuts import get_object_or_404

from recipes.models import IngredientInRecipe
from .models import ShoppingCart


def create_shopping_cart(request):

    user = request.user
    cart = get_object_or_404(ShoppingCart, user=user)

    ingredients = IngredientInRecipe.objects.filter(
        recipes__in_shopping_cart__user=request.user
    ).values('ingredient', 'amount')

    # .annotate(total_amount=sum('amount'))

    # recipes = cart.recipes.all()

    # ingredients = dict()
    # for recipe in recipes:
    #     for ing_obj in recipe.ingredients.all():
    #         ingredient = str(ing_obj.ingredient)
    #     ingredients[ingredient] = ingredients.get(
    #         ingredient,
    #         0
    #     ) + ing_obj.amount



    body_text = ''
    print(ingredients)
    for ingr, amount in ingredients:
        print(ingr, amount)
        body_text += f'{ingr.name} - {amount}\n'
    file = ('Cписок покупок пользователя '
            f'{user.first_name} {user.last_name}:\n\n'
            + body_text)
    file_name = f'список_покупок_{user.username}'
    return (file, file_name)
