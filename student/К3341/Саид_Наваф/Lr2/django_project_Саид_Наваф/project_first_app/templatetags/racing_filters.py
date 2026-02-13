from django import template

register = template.Library()

@register.filter
def filter_by_race(registrations, race):
    return [r for r in registrations if r.race == race]

@register.filter
def filter_by_team(cars, team):
    return [car for car in cars if car.team == team]