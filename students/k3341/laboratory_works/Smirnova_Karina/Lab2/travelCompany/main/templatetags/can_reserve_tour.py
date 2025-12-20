from django import template

register = template.Library()

@register.filter
def can_reserve_tour(reservation):
    """Проверяет, может ли пользователь снова забронировать тур:
        1. если нет заявок
        2. или если последняя заявка не в статусе waiting/approved
    """
    if not reservation or len(reservation) == 0:
        return True

    last = sorted(reservation, key=lambda r: r.reserved_at, reverse=True)[0]
    return last.status not in ['waiting', 'approved']