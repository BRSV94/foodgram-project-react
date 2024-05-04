from django.db.models import Sum
from django.shortcuts import get_object_or_404

from recipes.models import IngredientInRecipe
from .models import ShoppingCart


def create_shopping_cart(request):
    user = request.user
    ingredients = IngredientInRecipe.objects.filter(
        recipes__in_shopping_cart__user=user
    ).annotate(total_amount=Sum('amount')).values_list(
        'ingredient__name',
        'ingredient__measurement_unit__measurement_unit',
        'total_amount'
    ).order_by('ingredient__name')

    body_text = ''
    for name, measurement_unit, amount in ingredients:
        body_text += f'{name} - {amount} {measurement_unit}.\n'
    file = ('Cписок покупок пользователя '
            f'{user.first_name} {user.last_name}:\n\n'
            + body_text)
    file_name = f'список_покупок_{user.username}'
    return (file, file_name)
