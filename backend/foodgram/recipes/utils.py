def PositiveAmountValidator(value):
    if value < 1:
        raise ValueError(
            "Значение не может быть отрицательным."
        )