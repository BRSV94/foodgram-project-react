import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, MeasurementUnit


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('../data/ingredients.json', 'r') as file:
            data = json.load(file)
            for ing in data:
                name = ing['name']
                unit = ing['measurement_unit']

                meas_unit, create = MeasurementUnit.objects.get_or_create(
                    measurement_unit=unit
                )
                Ingredient.objects.create(
                    name=name,
                    measurement_unit=meas_unit
                )
