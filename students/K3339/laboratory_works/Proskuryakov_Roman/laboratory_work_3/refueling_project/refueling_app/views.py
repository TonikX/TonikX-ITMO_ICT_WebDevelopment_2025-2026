from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class FuelReferenceViewSet(ModelViewSet):
    queryset = FuelReference.objects.all()
    serializer_class = FuelReferenceSerializer

class CompaniesViewSet(ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer

class ProducedFuelViewSet(ModelViewSet):
    queryset = ProducedFuel.objects.select_related(
        "id_kind_fuel", "id_company"
    )
    serializer_class = ProducedFuelSerializer

class GasStationViewSet(ModelViewSet):
    queryset = GasStation.objects.select_related("id_company")
    serializer_class = GasStationSerializer

class SoldFuelViewSet(ModelViewSet):
    queryset = SoldFuel.objects.select_related(
        "id_produced_fuel", "id_station"
    )
    serializer_class = SoldFuelSerializer

class FuelPricesViewSet(ModelViewSet):
    queryset = FuelPrices.objects.select_related("id_sold_fuel")
    serializer_class = FuelPricesSerializer

class ClientsViewSet(ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer

class ClientCardsViewSet(ModelViewSet):
    queryset = ClientCards.objects.select_related(
        "id_client", "id_company"
    )
    serializer_class = ClientCardsSerializer

class SalesViewSet(ModelViewSet):
    queryset = Sales.objects.select_related(
        "id_fuel_price", "id_card"
    )
    serializer_class = SalesSerializer

class FuelPricesByStationView(APIView):
    def get(self, request):
        user = request.user
        station = user.id_station

        if not station:
            return Response({"detail": "User is not assigned to a gas station"}, status=400)

        now = timezone.now()

        # Получаем все продаваемое топливо на этой станции
        sold_fuel_qs = SoldFuel.objects.filter(id_station=station)
        
        # Получаем цены на это топливо
        # Фильтруем цены: start_time <= now и (end_time >= now или end_time is null)
        prices_qs = FuelPrices.objects.filter(
            id_sold_fuel__in=sold_fuel_qs
        ).filter(
            start_time__lte=now
        ).filter(
            Q(end_time__isnull=True) | Q(end_time__gt=now)
        )

        serializer = FuelPricesSerializer(prices_qs, many=True)
        return Response(serializer.data)
    

def calcPayment(initial_amount, card):
    now = timezone.now().date()  # сравниваем только даты

    # Проверка активности карты
    if card.start_date > now or (card.end_date and card.end_date <= now):
        return Response({"detail": "Card is not active"}, status=400)

    # Рассчёт скидки
    percent_discount = (card.discount_percent / 100) * initial_amount
    rub_discount = card.discount_rub
    total_discount = percent_discount + rub_discount

    # Конечная сумма к оплате
    final_amount = max(initial_amount - total_discount, 0)

    # Проверка баланса
    sufficient_balance = card.balance >= final_amount

    serializer = PaymentCalculationResultSerializer(data={
        "final_amount": round(final_amount, 2),
        "sufficient_balance": sufficient_balance
    })
    serializer.is_valid(raise_exception=True)
    
    return Response(serializer.data)

class PaymentCalculationView(APIView):
    def post(self, request):
        serializer = PaymentCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            card = ClientCards.objects.get(id_card=data["id_card"])
        except ClientCards.DoesNotExist:
            return Response({"detail": "Card not found"}, status=404)
        
        return calcPayment(data["initial_amount"], card)

class FuelPaymentCalculationView(APIView):
    def post(self, request):
        serializer = FuelPurchaseCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Получаем цену топлива
        try:
            fuel_price = FuelPrices.objects.get(id_fuel_price=data["id_fuel_price"])
        except FuelPrices.DoesNotExist:
            return Response({"detail": "Fuel price not found"}, status=404)

        # Получаем карту клиента
        try:
            card = ClientCards.objects.get(id_card=data["id_card"])
        except ClientCards.DoesNotExist:
            return Response({"detail": "Card not found"}, status=404)

        # Исходная сумма = цена за литр * количество литров
        initial_amount = fuel_price.per_liter * data["liters"]
        return calcPayment(initial_amount, card)

class FuelPaymentExecuteView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = FuelPurchaseCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Получаем цену топлива
        try:
            fuel_price = FuelPrices.objects.get(id_fuel_price=data["id_fuel_price"])
        except FuelPrices.DoesNotExist:
            return Response({"success": False, "detail": "Fuel price not found"})

        # Получаем карту клиента и блокируем запись для безопасного списания
        try:
            card = ClientCards.objects.select_for_update().get(id_card=data["id_card"])
        except ClientCards.DoesNotExist:
            return Response({"success": False, "detail": "Card not found"})

        now = timezone.now().date()
        # Проверка активности карты
        if card.start_date > now or (card.end_date and card.end_date <= now):
            return Response({"success": False, "detail": "Card is not active"})

        # Расчёт суммы
        initial_amount = fuel_price.per_liter * data["liters"]
        percent_discount = (card.discount_percent / 100) * initial_amount
        rub_discount = card.discount_rub
        total_discount = percent_discount + rub_discount
        final_amount = max(initial_amount - total_discount, 0)

        # Проверка баланса
        if card.balance < final_amount:
            return Response({"success": False, "detail": "Insufficient balance"})

        # --- Создаём продажу и списываем баланс ---
        card.balance -= final_amount
        card.save()

        Sales.objects.create(
            id_fuel_price=fuel_price,
            id_card=card,
            sale_date=timezone.now(),
            sold_liters_volume=data["liters"]
        )

        return Response({"success": True})
