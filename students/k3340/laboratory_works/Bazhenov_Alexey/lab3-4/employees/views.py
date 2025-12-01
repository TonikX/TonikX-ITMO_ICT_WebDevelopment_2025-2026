from datetime import date

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from stays.models import Stay
from .models import CleaningAssignment, Employee
from .serializers import CleaningAssignmentSerializer, EmployeeSerializer, ScheduleSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.prefetch_related('assignments')
    serializer_class = EmployeeSerializer

    @action(detail=True, methods=['post'], url_path='fire')
    def fire_employee(self, request, pk=None):
        employee = self.get_object()
        if employee.status == Employee.Status.FIRED:
            return Response({'detail': 'Сотрудник уже уволен.'}, status=status.HTTP_400_BAD_REQUEST)
        employee.status = Employee.Status.FIRED
        employee.termination_date = date.today()
        employee.save(update_fields=['status', 'termination_date'])
        return Response(self.get_serializer(employee).data)

    @action(detail=True, methods=['put'], url_path='schedule')
    def update_schedule(self, request, pk=None):
        employee = self.get_object()
        serializer = ScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee.assignments.all().delete()
        assignments = [
            CleaningAssignment(employee=employee, **entry)
            for entry in serializer.validated_data['assignments']
        ]
        CleaningAssignment.objects.bulk_create(assignments)
        employee.refresh_from_db()
        return Response(self.get_serializer(employee).data)

    @action(detail=False, methods=['get'], url_path='who-cleans')
    def who_cleans(self, request):
        client_id = request.query_params.get('client_id')
        weekday = request.query_params.get('weekday')
        if not client_id or not weekday:
            return Response({'detail': 'Нужны параметры client_id и weekday.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            weekday = weekday.lower()
        except AttributeError:
            return Response({'detail': 'Некорректное значение weekday.'}, status=status.HTTP_400_BAD_REQUEST)

        if weekday not in dict(CleaningAssignment.WEEKDAYS):
            return Response({'detail': 'Недопустимое значение weekday.'}, status=status.HTTP_400_BAD_REQUEST)

        stay = Stay.objects.filter(client_id=client_id, status=Stay.Status.ACTIVE).select_related('room').first()
        if not stay:
            return Response({'detail': 'Для клиента нет активного проживания.'}, status=status.HTTP_404_NOT_FOUND)

        assignment = CleaningAssignment.objects.select_related('employee').filter(
            floor=stay.room.floor,
            weekday=weekday,
        ).first()

        if not assignment:
            return Response({'detail': 'На указанном этаже нет назначенного сотрудника.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(EmployeeSerializer(assignment.employee).data)
