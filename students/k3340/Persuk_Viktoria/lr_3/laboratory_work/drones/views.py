from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from .models import Drones, Flights, FlightLogs, Documents
from .serializer import DroneSerializer, FlightSerializer, FlightLogSerializer, DocumentSerializer


class AuthenticatedModelViewSet(viewsets.ModelViewSet):
    """
    Базовый класс: требуем аутентификацию (Token/Session)
    """
    permission_classes = [permissions.IsAuthenticated]


class DroneViewSet(AuthenticatedModelViewSet):
    """
    CRUD операции для дронов
    Поддерживает вложенный доступ через /drones/<id>/flights/ и /drones/<id>/documents/
    """

    serializer_class = DroneSerializer


    def get_queryset(self):
        """
        Получение списка дронов
        """
        return (
            Drones.objects.all()
            .prefetch_related("flights", "documents")
            .order_by("id")
        )


class FlightViewSet(AuthenticatedModelViewSet):
    """
    CRUD операции для полётов
    Поддерживает фильтрацию по дрону при использовании вложенного роутера
    """

    serializer_class = FlightSerializer


    def get_queryset(self):
        """
        Получение списка полётов для дрона
        """
        queryset = Flights.objects.select_related("drone_id").prefetch_related("logs").order_by("-start_datetime")
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            queryset = queryset.filter(drone_id_id=drone_pk)
        return queryset


    def perform_create(self, serializer):
        """
        Создание полёта для дрона
        """
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            drone = get_object_or_404(Drones, pk=drone_pk)
            serializer.save(drone_id=drone)
        else:
            serializer.save()


class FlightLogViewSet(AuthenticatedModelViewSet):
    """
    CRUD операции для журналов полётов
    Поддерживает вложенный доступ через /flights/<id>/logs/
    """

    serializer_class = FlightLogSerializer


    def get_queryset(self):
        """
        Получение списка журналов полётов для дрона
        """
        queryset = FlightLogs.objects.select_related("flight_id", "flight_id__drone_id").order_by("-timestamp")
        flight_pk = self.kwargs.get("flight_pk")
        if flight_pk:
            queryset = queryset.filter(flight_id_id=flight_pk)
        return queryset


    def perform_create(self, serializer):
        """
        Создание журнала полёта
        """
        flight_pk = self.kwargs.get("flight_pk")
        if flight_pk:
            flight = get_object_or_404(Flights, pk=flight_pk)
            serializer.save(flight_id=flight)
        else:
            serializer.save()


class DocumentViewSet(AuthenticatedModelViewSet):
    """
    CRUD операции для документов
    Поддерживает вложенный доступ через /drones/<id>/documents/
    """

    serializer_class = DocumentSerializer

    def get_queryset(self):
        """
        Получение списка документов для дрона
        """
        queryset = Documents.objects.select_related("drone_id").order_by("-uploaded_at")
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            queryset = queryset.filter(drone_id_id=drone_pk)
        return queryset


    def perform_create(self, serializer):
        """
        Создание документа для дрона
        """
        drone_pk = self.kwargs.get("drone_pk")
        if drone_pk:
            drone = get_object_or_404(Drones, pk=drone_pk)
            serializer.save(drone_id=drone)
        else:
            serializer.save()
