from datetime import date
from decimal import Decimal

from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Room, Stay


def quarter_range(year: int, q: int):
    mapping = {
        1: (date(year, 1, 1), date(year, 3, 31)),
        2: (date(year, 4, 1), date(year, 6, 30)),
        3: (date(year, 7, 1), date(year, 9, 30)),
        4: (date(year, 10, 1), date(year, 12, 31)),
    }
    if q not in mapping:
        raise ValueError("q must be 1..4")
    return mapping[q]


def stay_days_in_period(check_in: date, check_out, start: date, end: date) -> int:
    """Сколько оплачиваемых дней проживания попало в период (включительно)"""
    out = check_out if check_out is not None else end
    s = max(check_in, start)
    e = min(out, end)
    if e < s:
        return 0
    return (e - s).days + 1


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def quarter_report(request):
    q_str = request.query_params.get("q")
    if not q_str:
        return Response({"error": "q is required (1..4)"}, status=400)

    try:
        q = int(q_str)
        year = date.today().year
        start, end = quarter_range(year, q)
    except Exception:
        return Response({"error": "q must be integer 1..4"}, status=400)

    # 2) Кол-во номеров на каждом этаже
    rooms_per_floor = list(
        Room.objects.values("floor")
        .annotate(rooms_count=Count("id"))
        .order_by("floor")
    )

    # Берем проживания, которые пересекаются с кварталом
    stays = (
        Stay.objects.select_related("room", "client")
        .filter(check_in__lte=end)
        .exclude(check_out__lt=start)   # выехали до начала квартала
    )

    room_to_clients = {}
    room_income = {}

    for s in stays:
        days = stay_days_in_period(s.check_in, s.check_out, start, end)
        if days <= 0:
            continue

        room_to_clients.setdefault(s.room_id, set()).add(s.client_id)
        room_income[s.room_id] = room_income.get(s.room_id, Decimal("0")) + (
            Decimal(days) * s.room.price_per_day
        )

    per_room = []
    total_income = Decimal("0")

    for r in Room.objects.all().order_by("number"):
        clients_count = len(room_to_clients.get(r.id, set()))
        income = room_income.get(r.id, Decimal("0"))
        total_income += income

        per_room.append({
            "room_number": r.number,
            "floor": r.floor,
            "clients_count": clients_count,
            "income": str(income),
        })

    return Response({
        "year": year,
        "quarter": q,
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "rooms_per_floor": rooms_per_floor,
        "per_room": per_room,
        "total_income": str(total_income),
    })