# from aspose import pdf
from django.shortcuts import get_object_or_404

from .models import ShoppingCart


def create_shopping_cart(request):
    # '''
    # Функция возвращает кортеж (PDF-файл, имя файла).
    # '''
    # '''
    # https://blog.aspose.com/ru/pdf/create-pdf-files-in-python/
    # '''

    user = request.user
    cart = get_object_or_404(ShoppingCart, user=user)
    recipes = cart.recipes.all()
    # file = pdf.Document()
    # page = file.pages.add()
    # title_text = pdf.text.TextFragment(
    #     f'Список покупок пользователя {user}:\n\n'
    # )
    # page.paragraphs.add(title_text)

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
#     body_text_fragment = pdf.text.TextFragment(body_text)
#     page.paragraphs.add(body_text_fragment)
    file = (f'Cписок_покупок_{user.username}'
            + body_text)
    print(file)
    file_name = f'список_покупок_{user.username}.pdf'
#     file.save(file_name)
    return (file, file_name)
