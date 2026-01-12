from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from decimal import Decimal
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
    # Подключаем бэкенд фильтрации
    filter_backends = [DjangoFilterBackend]
    # Указываем поля, по которым можно фильтровать
    filterset_fields = ['phone_number']

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
        
        print("now_time", now)

        # Получаем цены на это топливо
        # Фильтруем цены: start_time <= now и (end_time > now или end_time is null)
        prices_qs = FuelPrices.objects.filter(
            id_sold_fuel__in=sold_fuel_qs
        ).filter(
            start_time__lte=now
        ).filter(
            Q(end_time__isnull=True) | Q(end_time__gt=now)
        )

        serializer = FuelPricesSerializer(prices_qs, many=True)
        return Response(serializer.data)

# рассчитывает цену для конкретной карты (не проверяет карту)
def calcPayment(initial_amount, card):
    initial_amount = Decimal(initial_amount)

    # Рассчёт скидки
    percent_discount = (card.discount_percent / 100) * initial_amount
    rub_discount = card.discount_rub
    total_discount = percent_discount + rub_discount

    # Конечная сумма к оплате
    final_amount = max(initial_amount - total_discount, 0)

    return final_amount

def paymentCalculationResult(initial_amount, card_id):
    card = ClientCards.getById(card_id)
    if (isinstance(card, Response)):
        return card

    final_amount = calcPayment(initial_amount, card)

    # Проверка баланса
    sufficient_balance = card.balance >= final_amount

    serializer = PaymentCalculationResultSerializer(data={
        "final_amount": final_amount,
        "sufficient_balance": sufficient_balance
    })
    serializer.is_valid(raise_exception=True)
    
    return Response(serializer.data)

class PaymentCalculationView(APIView):
    def post(self, request):
        serializer = PaymentCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return paymentCalculationResult(data["initial_amount"], data["id_card"])

class FuelPaymentCalculationView(APIView):
    def post(self, request):
        serializer = FuelPurchaseCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Получаем цену топлива
        fuel_price = FuelPrices.getById(data["id_fuel_price"])
        if (isinstance(fuel_price, Response)):
            return fuel_price

        # Исходная сумма = цена за литр * количество литров
        initial_amount = fuel_price.per_liter * data["liters"]
        return paymentCalculationResult(initial_amount, data["id_card"])

class FuelPaymentExecuteView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = FuelPurchaseCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Получаем цену топлива
        fuel_price = FuelPrices.getById(data["id_fuel_price"])
        if (isinstance(fuel_price, Response)):
            fuel_price.data['success'] = False
            fuel_price.status_code = 200
            return fuel_price

        # Получаем карту клиента
        card = ClientCards.getById(data["id_card"])
        if (isinstance(card, Response)):
            card.data['success'] = False
            card.status_code = 200
            return card

        # Расчёт суммы
        initial_amount = fuel_price.per_liter * Decimal(data["liters"])
        final_amount = calcPayment(initial_amount, card)

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
            sold_liters_volume=data["liters"],
            amount_paid = final_amount
        )

        return Response({"success": True})


from django.db.models import Avg, Min, Max, Sum, Count

class SalesQueryBuilder:
    """Класс для построения запросов с агрегацией по продажам"""
    
    # Маппинг моделей на пути до sales
    ANNOTATE_PREFIX_PATHS = {
        ClientCards: 'sales',
        Clients: 'client_cards__sales',
        Companies: 'client_cards__sales',
        
        FuelPrices: 'sales',
        SoldFuel: 'fuel_prices__sales',
        ProducedFuel: 'sold_fuel__fuel_prices__sales',
        GasStation: 'sold_fuel__fuel_prices__sales',
        FuelReference: 'produced_fuel__sold_fuel__fuel_prices__sales',
    }
    
    AGGREGATIONS = {
        'total_amount': {
            'func': models.Sum,
            'field': 'amount_paid'
        },
        'total_liters': {
            'func': models.Sum,
            'field': 'sold_liters_volume'
        },
        'sales_count': {
            'func': models.Count,
            'field': 'id_sales'
        },
        'avg_liters': {
            'func': models.Avg,
            'field': 'sold_liters_volume'
        },
    }
    
    @classmethod
    def build_query(self, model_type, columns, aggregations=None, start_time=None, end_time=None):
        """
        Строит агрегирующий запрос
        
        Args:
            model_type: Класс модели Django
            columns: Список полей для SELECT
            aggregations: Список агрегаций (по умолчанию: total_amount, sales_count, avg_liters)
            start_time: начало периода продаж
            end_time: конец периода продаж
        """
        path = self.ANNOTATE_PREFIX_PATHS[model_type]
        if path is None:
            raise ValueError(f"Модель {model_type.__name__} не связана с Sales")
        
        # Строим фильтр для этой агрегации
        filter_kwargs = {}
        
        # Если хотя бы одна граница указана, создаем фильтр
        if start_time is not None or end_time is not None:
            filter_q = Q()
            
            if start_time is not None:
                filter_q &= Q(**{f'{path}__sale_date__gte': start_time})
            
            if end_time is not None:
                filter_q &= Q(**{f'{path}__sale_date__lte': end_time})
            
            filter_kwargs['filter'] = filter_q
        
        if aggregations is None or not aggregations:
            aggregations = ['total_amount', 'sales_count', 'avg_liters']

        # Создаем annotate параметры
        annotate_kwargs = {}
        for agg_name in aggregations:
            if agg_name not in self.AGGREGATIONS:
                continue
                
            agg_config = self.AGGREGATIONS[agg_name]
            field_name = agg_config['field']
            
            # Строим полный путь до поля
            lookup_field = f'{path}__{field_name}'
            
            # Создаем агрегационную функцию с фильтром или без
            if filter_kwargs:
                annotate_kwargs[agg_name] = agg_config['func'](lookup_field, **filter_kwargs)
            else:
                annotate_kwargs[agg_name] = agg_config['func'](lookup_field)
        
        # Строим запрос
        query = model_type.objects.annotate(**annotate_kwargs)
        
        # # Применяем фильтр по времени для связанных записей
        # if time_filter:
        #     query = query.filter(time_filter)

        # Подготавливаем values
        values_fields = list(columns) + list(annotate_kwargs.keys())
        
        return query.values(*values_fields)

class SalesSummaryByModelView(APIView):
    MODEL_TYPE_BY_NAME = {
        'fuel_reference': FuelReference,
        'companies': Companies,
        'produced_fuel': ProducedFuel,
        'gas_stations': GasStation,
        'sold_fuel': SoldFuel,
        'fuel_prices': FuelPrices,
        'clients': Clients,
        'client_cards': ClientCards,
    }

    def get(self, request, model_name):
        if (not model_name in self.MODEL_TYPE_BY_NAME):
            return Response({"detail": f"There is no table with name '{model_name}'"}, status=404)

        model_type = self.MODEL_TYPE_BY_NAME[model_name]

        serializer = SalesSummaryQueryParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        hidden_columns = serializer.validated_data.get('hidden_columns', [])
        aggregations = serializer.validated_data.get('aggregations', [])
        aggregations = None # сериализатор пока не умею другой набор агрегирующих колонок кроме стандартных
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')

        columns = set(get_model_field_names(model_type)) - set(hidden_columns)

        query = SalesQueryBuilder.build_query(model_type, columns, aggregations, start_time, end_time)
        
        print("query", str(query.query))

        model_serializer = create_model_serializer_with_sales_summary(model_type, hidden_columns)
        ser = model_serializer(query, many=True)

        return Response(ser.data)
    
# views.py (добавить новый класс)
class AvailableAggregationTablesView(APIView):
    """
    API для получения списка доступных таблиц для агрегации с русскими названиями
    """
    
    # Словарь с русскими названиями таблиц
    TABLE_NAMES_RU = {
        'fuel_reference': {
            'name': 'Видам топлива',
            'description': 'Типы и характеристики топлива'
        },
        'companies': {
            'name': 'Компаниям',
            'description': 'Производители и сети АЗС'
        },
        'produced_fuel': {
            'name': 'Производимому топливу',
            'description': 'Конкретные партии произведенного топлива'
        },
        'gas_stations': {
            'name': 'АЗС',
            'description': 'Автозаправочные станции'
        },
        'sold_fuel': {
            'name': 'Продаваемому топливу',
            'description': 'Топливо, доступное для продажи на АЗС'
        },
        'fuel_prices': {
            'name': 'Ценам на топливо',
            'description': 'История цен на топливо'
        },
        'clients': {
            'name': 'Клиентам',
            'description': 'Информация о клиентах'
        },
        'client_cards': {
            'name': 'Картам клиентов',
            'description': 'Карты клиентов для оплаты'
        },
    }
    
    def get(self, request):
        """
        Возвращает список доступных таблиц для агрегации
        """
        tables = []
        
        for key, value in self.TABLE_NAMES_RU.items():
            tables.append({
                'key': key,
                'name': value['name'],
                'description': value.get('description', '')
            })
        
        # Сортируем по русскому названию для удобства
        tables.sort(key=lambda x: x['name'])
        
        serializer = AvailableTableSerializer(tables, many=True)
        return Response(serializer.data)