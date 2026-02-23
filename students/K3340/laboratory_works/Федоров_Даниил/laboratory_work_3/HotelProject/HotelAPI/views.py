from rest_framework import viewsets, serializers, response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    #о клиентах, проживавших в заданном номере, в заданный период времени;
    @action(detail=False, methods=['get'])
    def room_history(self, request):
        room_number = request.query_params.get('room_number')
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        room = Room.objects.get(number=room_number)

        clients = room.clients.filter(
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        )


        return Response({
            'room': RoomSerializer(room).data,
            'clients': ClientSerializer(clients, many=True).data
        })
    #Сколько в гостинице свободных номеров;
    @action(detail=False, methods=['get'])
    def free_rooms(self, request):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        free_rooms = Room.objects.exclude(
            id__in=Client.objects.filter(
                check_in_date__lte=end_date,
                check_out_date__gte=start_date
            ).values('id')
        )

        return Response({'free_rooms': free_rooms.count()})




class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    #о количестве клиентов, прибывших из заданного города,
    @action(detail=False, methods=['get'])
    def clients_town_count(self, request):
        town = request.query_params.get('town')

        clients = Client.objects.filter(city_of_origin=town).count()

        return Response({'clients_count': clients})

    #Список клиентов с указанием места жительства, которые проживали в те же дни,
    #Что и заданный клиент, в определенный период времени.
    @action(detail=True, methods=['get'])
    def same_clients(self, request, pk=None):

        client = Client.objects.get(id=pk)
        start_date = client.check_in_date
        end_date = client.check_out_date

        clients = Client.objects.filter(
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        ).exclude(id=pk)

        clients_serializer = ClientSerializer(clients, many=True)
        return Response({
            'client': ClientSerializer(client).data,
            'same_clients': clients_serializer.data
        })



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    # о том, кто из служащих убирал номер указанного клиента в заданный день недели,
    @action(detail=False, methods=['get'])
    def cleaning_schedule(self, request):
        client_id = request.query_params.get('client_id')
        day = request.query_params.get('day')

        client = Client.objects.get(id=client_id)
        room = client.room

        cleaning_schedule =CleaningSchedule.objects.filter(
            floor=room.floor,
            day_of_week=day
        )
        serializer = CleaningScheduleWithEmployeeSerializer(cleaning_schedule, many=True)
        return Response({
            'client' : ClientSerializer(client).data,
            'cleaning_schedule': serializer.data
        })







