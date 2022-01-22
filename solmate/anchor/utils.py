import re


def camel_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def snake_to_camel(name):
    def _upper(m):
        return m.group(0)[1].upper()

    return re.sub(r"(?P<start>_[a-z])", _upper, name)


def pascal_to_snake(name):
    return camel_to_snake(name[0].lower() + name[1:])


def snake_to_pascal(name):
    pascal = snake_to_camel(name)
    return pascal[0].upper() + pascal[1:]


def kebab_to_snake(name):
    return re.sub("-", "_", name)


def snake_to_kebab(name):
    return re.sub("_", "-", name)
