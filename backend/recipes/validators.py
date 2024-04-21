from rest_framework import serializers


def ingredients_validator(self, ingredients):
    if not ingredients:
        raise serializers.ValidationError(
            "Необходимо указать ингредиенты.")
    ing_ids = []
    for ingredient in ingredients:
        if ingredient['id'] in ing_ids:
            raise serializers.ValidationError(
                "Ингредиенты не могут повторяться.")
        ing_ids.append(ingredient['id'])


def tags_validator(self, tags):
    if not tags:
        raise serializers.ValidationError(
            "Необходимо указать тэги.")
    if tags and len(tags) != len(set(tags)):
        raise serializers.ValidationError(
            "Тэги не могут повторяться.")


def image_validator(self, image):
    if image is None:
        raise serializers.ValidationError(
            "Необходимо загрузить изображение.")
