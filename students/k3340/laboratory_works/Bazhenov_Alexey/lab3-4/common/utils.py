from datetime import date

from django.utils.dateparse import parse_date


def parse_date_param(value: str, name: str) -> date:
    parsed = parse_date(value)
    if not parsed:
        raise ValueError(f'Некорректная дата в параметре "{name}". Используйте формат YYYY-MM-DD.')
    return parsed


def ensure_period(start: str | None, end: str | None) -> tuple[date, date]:
    if not start or not end:
        raise ValueError('Параметры start и end обязательны.')
    start_date = parse_date_param(start, 'start')
    end_date = parse_date_param(end, 'end')
    if start_date > end_date:
        raise ValueError('Дата начала должна быть не позже даты окончания.')
    return start_date, end_date

