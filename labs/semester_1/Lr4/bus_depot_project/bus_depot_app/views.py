from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg, Count
from .models import (
    BusType,
    Bus,
    Route,
    Driver,
    DriverAssignment,
    BusStatus,
)
from .serializers import (
    BusTypeSerializer,
    BusSerializer,
    RouteSerializer,
    DriverSerializer,
    DriverAssignmentSerializer,
    BusStatusSerializer,
    RouteDriversSerializer,
    TotalRouteLengthSerializer,
    BusStatusDetailSerializer,
    DriverClassStatsSerializer,
    ReportSerializer,
)


# ===== Базовые запросы =====


class BusTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для типа автобуса.
    """
    serializer_class = BusTypeSerializer
    queryset = BusType.objects.all()


class BusViewSet(viewsets.ModelViewSet):
    """
    ViewSet для автобуса.
    """
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet для маршрута.
    """
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet для водителя.
    """
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class DriverAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для назначения водителя.
    """
    serializer_class = DriverAssignmentSerializer
    queryset = DriverAssignment.objects.all()


class BusStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet для статуса автобуса.
    """
    serializer_class = BusStatusSerializer
    queryset = BusStatus.objects.all()


# ===== Специальные запросы =====

class RouteDriversAPIView(APIView):
    """
    Список водителей, работающих на определённом маршруте с указанием графика их работы.
    """
    def get(self, request, route_id):
        # Получаем маршрут
        try:
            route = Route.objects.get(pk=route_id)
        except Route.DoesNotExist:
            return Response(
                {"error": "Маршрут не найден"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем всех водителей, для которых этот маршрут является основным
        drivers = Driver.objects.filter(main_route=route).distinct()

        # Преобразуем данные в JSON
        serializer = RouteDriversSerializer({
            'route': route,
            'drivers': drivers
        })

        # Возвращаем данные
        return Response(serializer.data)


class TotalRouteLengthAPIView(APIView):
    """
    Общая протяжённость всех маршрутов.
    """
    def get(self, request):
        aggregation = Route.objects.aggregate(
            total_length=Sum('duration'),
            routes_count=Count('id'),
            average_length=Avg('duration')
        )
        if aggregation['total_length'] is None:
            aggregation['total_length'] = 0
            aggregation['routes_count'] = 0
            aggregation['average_length'] = 0
        serializer = TotalRouteLengthSerializer(aggregation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotActiveBusesAPIView(APIView):
    """
    Информация об автобусах, не вышедших на линию в заданную дату.
    (Дата задаётся в URL: .../?date=YYYY-MM-DD)
    """
    def get(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response(
                {"error": "Параметр 'date' обязателен (формат: YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        not_active_statuses = BusStatus.objects.filter(
            date=date
        ).exclude(
            status='active'
        ).select_related('bus')
        serializer = BusStatusDetailSerializer(not_active_statuses, many=True)
        return Response(serializer.data)


class DriverClassStatsAPIView(APIView):
    """
    API для получения статистики по количеству водителей каждого класса.
    """
    def get(self, request):
        stats = (
            Driver.objects.values('driver_class')
            .annotate(count=Count('id'))
            .order_by('driver_class')
        )
        for stat in stats:
            stat['driver_class_display'] = dict(Driver.CLASS_CHOICES).get(stat['driver_class'],
                                                                              'Неизвестный класс')
        serializer = DriverClassStatsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ===== Отчёт =====


class ReportAPIView(APIView):
    """
    API для получения отчёта по автобусному парку.
    """
    def get(self, request):
        # Получаем общую статистику
        summary_data = self.get_summary_data()

        # Получаем данные по маршрутам
        routes_data = self.get_routes_data()

        # Преобразуем полученные данные с помощью сериализатора и возвращаем
        report_data = {
            'summary': summary_data,
            'routes': routes_data
        }
        serializer = ReportSerializer(report_data)
        return Response(serializer.data)

    def get_summary_data(self):
        """
        Формирование общей статистики.
        """
        # Рассчитываем различные total-значения
        total_routes = Route.objects.count()
        total_route_length_minutes = Route.objects.aggregate(
            total=Sum('duration')
        )['total'] or 0
        total_bus_types = BusType.objects.count()
        total_buses = Bus.objects.count()
        total_drivers = Driver.objects.count()

        # Рассчитываем распределение типов автобусов
        bus_type_distribution = {}
        for bus_type in BusType.objects.all():
            count = Bus.objects.filter(bus_type=bus_type).count()
            bus_type_distribution[bus_type.name] = count
        
        # Рассчитываем средний стаж водителя
        drivers_avg_experience = Driver.objects.aggregate(
            avg_exp=Avg('experience')
        )['avg_exp'] or 0

        # Рассчитываем распределение водителей по классам
        drivers_class_distribution = {
            '1': Driver.objects.filter(driver_class='1').count(),
            '2': Driver.objects.filter(driver_class='2').count(),
            '3': Driver.objects.filter(driver_class='3').count()
        }

        # Возвращаем полученные данные
        return {
            'total_routes': total_routes,
            'total_route_length_minutes': total_route_length_minutes,
            'total_bus_types': total_bus_types,
            'bus_type_distribution': bus_type_distribution,
            'total_buses': total_buses,
            'total_drivers': total_drivers,
            'drivers_average_experience': round(drivers_avg_experience, 1),
            'drivers_class_distribution': drivers_class_distribution
        }

    def get_routes_data(self):
        """
        Сбор данных для всех маршрутов.
        """
        # Перебираем все маршруты, для каждого маршрута получаем данные
        # и возвращаем полученные результаты
        routes_data = []
        for route in Route.objects.all():
            route_data = self.get_route_data(route)
            routes_data.append(route_data)
        return routes_data

    def get_route_data(self, route):
        """
        Получение данных для конкретного маршрута.
        """
        # Требуемые данные маршрута
        route_data = {
            'id': route.id,
            'number': route.number,
            'start_point': route.start_point,
            'end_point': route.end_point,
            'start_time': route.start_time,
            'end_time': route.end_time,
            'interval': route.interval,
            'duration': route.duration,
            'bus_types': []
        }

        # Получаем всех водителей для данного маршрута
        route_drivers = Driver.objects.filter(main_route=route)

        # Словарь для данных по типам автобусов на данном маршруте
        bus_types_data = {}

        # Перебираем всех водителей
        for driver in route_drivers:
            # Если у водителя нет главного автобуса, то пропускаем итерацию
            if driver.main_bus is None:
                continue

            # Получаем главный автобус водителя и тип этого автобуса 
            bus = driver.main_bus
            bus_type = bus.bus_type

            # Если этого типа нет в словаре типов автобусов, то добавляем
            if bus_type.id not in bus_types_data:
                bus_types_data[bus_type.id] = {
                    'id': bus_type.id,
                    'name': bus_type.name,
                    'capacity': bus_type.capacity,
                    'buses': {}
                }
            
            # Если автобус не добавлен в словарь автобусов данного типа, то добавляем
            if bus.id not in bus_types_data[bus_type.id]['buses']:
                bus_types_data[bus_type.id]['buses'][bus.id] = {
                    'id': bus.id,
                    'license_plate': bus.license_plate,
                    'is_active': bus.is_active,
                    'purchase_date': bus.purchase_date,
                    'drivers': []
                }
            
            # Формируем данные для водителя и добавляем в список водителей данного автобуса
            driver_data = {
                'id': driver.id,
                'full_name': driver.full_name,
                'passport': driver.passport,
                'birth_date': driver.birth_date,
                'driver_class': driver.driver_class,
                'experience': driver.experience,
                'salary': driver.salary
            }
            bus_types_data[bus_type.id]['buses'][bus.id]['drivers'].append(driver_data)

        # Преобразуем словари в списки и добавляем к данным маршрута
        for bus_type_id, bus_type_data in bus_types_data.items():
            buses_list = list(bus_type_data['buses'].values())
            route_data['bus_types'].append({
                'id': bus_type_data['id'],
                'name': bus_type_data['name'],
                'capacity': bus_type_data['capacity'],
                'buses': buses_list
            })

        # Возвращаем данные маршрута
        return route_data
