from datetime import date, datetime
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Stay, Client, CleaningSchedule, Room


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def free_rooms_count(request):
    date_str = request.query_params.get("date")
    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        target_date = date.today()

    occupied_room_ids = Stay.objects.filter(
        check_in__lte=target_date
    ).filter(
        Q(check_out__isnull=True) | Q(check_out__gte=target_date)
    ).values_list("room_id", flat=True)

    free = Room.objects.exclude(id__in=occupied_room_ids).count()

    return Response({
        "date": target_date.isoformat(),
        "free_rooms": free
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def who_cleaned_client_room(request):
    client_id = request.query_params.get("client_id")
    date_str = request.query_params.get("date")  # YYYY-MM-DD

    if not client_id or not date_str:
        return Response({"error": "client_id and date are required"}, status=400)

    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    weekday = target_date.weekday()

    stay = Stay.objects.select_related("room", "client").filter(
        client_id=client_id,
        check_in__lte=target_date
    ).filter(
        Q(check_out__isnull=True) | Q(check_out__gte=target_date)
    ).first()

    if not stay:
        return Response(
            {"error": "client did not live in hotel on this date"},
            status=404
        )

    floor = stay.room.floor

    schedules = CleaningSchedule.objects.select_related("employee").filter(
        floor=floor,
        weekday=weekday,
        employee__is_active=True
    )

    employees = []
    for s in schedules:
        employees.append({
            "employee_id": s.employee.id,
            "last_name": s.employee.last_name,
            "first_name": s.employee.first_name,
            "patronymic": s.employee.patronymic,
            "floor": s.floor,
            "weekday": s.weekday,
        })

    return Response({
        "client_id": int(client_id),
        "date": date_str,
        "weekday": weekday,
        "room_number": stay.room.number,
        "room_floor": floor,
        "employees": employees
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def clients_in_room_period(request):
    room_number = request.query_params.get("room_number")
    start = request.query_params.get("start")
    end = request.query_params.get("end")

    if not room_number or not start or not end:
        return Response(
            {"error": "room_number, start, end are required"},
            status=400
        )

    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    stays = Stay.objects.select_related("client", "room").filter(
        room__number=room_number,
        check_in__lte=end_date
    ).filter(
        Q(check_out__isnull=True) | Q(check_out__gte=start_date)
    )

    result = []
    for stay in stays:
        result.append({
            "client_id": stay.client.id,
            "passport_number": stay.client.passport_number,
            "last_name": stay.client.last_name,
            "first_name": stay.client.first_name,
            "check_in": stay.check_in,
            "check_out": stay.check_out,
        })

    return Response({
        "room_number": room_number,
        "period": {"start": start, "end": end},
        "clients": result
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def clients_from_city(request):
    city = request.query_params.get("city")

    if not city:
        return Response({"error": "city is required"}, status=400)

    count = Client.objects.filter(city_from__iexact=city).count()

    return Response({
        "city": city,
        "clients_count": count
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def clients_overlap(request):
    client_id = request.query_params.get("client_id")
    start = request.query_params.get("start")
    end = request.query_params.get("end")

    if not client_id or not start or not end:
        return Response({"error": "client_id, start, end are required"}, status=400)

    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    # Проживания заданного клиента, которые пересекаются с периодом
    base_stays = Stay.objects.filter(
        client_id=client_id,
        check_in__lte=end_date
    ).filter(
        Q(check_out__isnull=True) | Q(check_out__gte=start_date)
    )

    if not base_stays.exists():
        return Response({
            "client_id": int(client_id),
            "period": {"start": start, "end": end},
            "overlap_clients": []
        })

    overlap_ids = set()

    # Для каждого проживания клиента ищем других, кто пересекается по датам
    for s in base_stays:
        s_start = max(s.check_in, start_date)
        s_end = min(s.check_out or end_date, end_date)

        other_stays = Stay.objects.filter(
            check_in__lte=s_end
        ).filter(
            Q(check_out__isnull=True) | Q(check_out__gte=s_start)
        ).exclude(client_id=client_id)

        overlap_ids.update(other_stays.values_list("client_id", flat=True))

    from .models import Client
    clients = Client.objects.filter(id__in=overlap_ids).order_by("last_name", "first_name")

    result = []
    for c in clients:
        result.append({
            "client_id": c.id,
            "last_name": c.last_name,
            "first_name": c.first_name,
            "address": c.address,
            "city_from": c.city_from,
            "passport_number": c.passport_number,
        })

    return Response({
        "client_id": int(client_id),
        "period": {"start": start, "end": end},
        "overlap_clients": result
    })