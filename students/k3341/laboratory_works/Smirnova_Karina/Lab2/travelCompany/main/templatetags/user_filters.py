from django import template

register = template.Library()

@register.filter
def is_admin(user):
    """Проверяет, является ли пользователь администратором или staff"""

    return user.groups.filter(name='Администратор').exists() or user.is_staff