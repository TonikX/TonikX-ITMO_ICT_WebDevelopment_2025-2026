from django import template

register = template.Library()

@register.filter
def filter_by_race(registrations, race):
    return [r for r in registrations if r.race == race]

@register.filter
def filter_by_team(cars, team):
    return [car for car in cars if car.team == team]

# Add a filter to add a CSS class to form fields
from django import forms

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={**field.field.widget.attrs, 'class': css_class})