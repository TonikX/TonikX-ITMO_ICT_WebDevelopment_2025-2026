from django import template

register = template.Library()

@register.filter
def get_item(dct, key):
    if dct is None:
        return None
    return dct.get(key)

@register.filter
def get_grade(grade_map, key):
    if grade_map is None:
        return None
    return grade_map.get(key)
