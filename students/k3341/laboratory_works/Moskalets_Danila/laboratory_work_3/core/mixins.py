from django.utils import timezone
from .models import ServiceDiscount


class CurrentDiscountMixin:
    """
    Универсальная логика получения скидки:
    - активная
    - ближайшая будущая
    - последняя прошедшая
    """

    def get_current_discount(self, obj):
        now = timezone.now()

        active = ServiceDiscount.objects.filter(
            service=obj,
            start_date__lte=now,
            end_date__gte=now
        ).order_by('-end_date').first()

        if active:
            return {
                'id': active.id,
                'discount_percent': str(active.discount_percent),
                'start_date': active.start_date,
                'end_date': active.end_date
            }

        future = ServiceDiscount.objects.filter(
            service=obj,
            start_date__gt=now
        ).order_by('start_date').first()

        if future:
            return {
                'id': future.id,
                'discount_percent': str(future.discount_percent),
                'start_date': future.start_date,
                'end_date': future.end_date,
                'starts_in': f"Скидка начнется {future.start_date.strftime('%d.%m.%Y')}"
            }

        past = ServiceDiscount.objects.filter(
            service=obj,
            end_date__lt=now
        ).order_by('-end_date').first()

        if past:
            return {
                'id': past.id,
                'discount_percent': str(past.discount_percent),
                'start_date': past.start_date,
                'end_date': past.end_date,
                'status': 'ended',
                'ended_at': f"Скидка закончилась {past.end_date.strftime('%d.%m.%Y')}"
            }

        return None
