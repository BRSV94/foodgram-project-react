

def tags_validator(value):
    if not value:
        raise ValueError("Значение не может быть пустым.")