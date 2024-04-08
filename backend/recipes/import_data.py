import json
from recipes.models import Ingredient, MeasurementUnit


def import_data():
    with open('../../data/ingredients.json', 'r') as file:
        data = json.load(file)
        for ingredient in data:
            # {"name": "абрикосовое варенье", "measurement_unit": "г"}
            name = ingredient['name']
            measurement_unit = ingredient['measurement_unit']
            unit_obj = MeasurementUnit.objects.get_or_create(
                measurement_unit=measurement_unit
            )
            Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=unit_obj
            )
    print('Данные ингредиентов успешно добавлены в бд.')
