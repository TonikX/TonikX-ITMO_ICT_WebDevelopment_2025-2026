from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Получить значение из словаря по ключу.
    Используется в шаблонах для доступа к элементам словаря.
    """
    return dictionary.get(key)


@register.filter
def count_late(submissions):
    """
    Подсчитать количество просроченных заданий
    """
    count = 0
    for submission in submissions:
        if submission.is_late:
            count += 1
    return count
