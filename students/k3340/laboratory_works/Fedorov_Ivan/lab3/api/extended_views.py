# api/extended_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from hotel.models import Room, Client, Employee, CleaningSchedule


class HotelStatisticsView(APIView):
    """Статистика гостиницы"""

    def get(self, request):
        # Общая статистика
        total_rooms = Room.objects.count()
        available_rooms = Room.objects.filter(is_available=True).count()
        occupied_rooms = total_rooms - available_rooms

        total_clients = Client.objects.count()
        current_clients = Client.objects.filter(check_out_date__isnull=True).count()

        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(is_active=True).count()

        statistics = {
            'rooms': {
                'total': total_rooms,
                'available': available_rooms,
                'occupied': occupied_rooms,
                'occupancy_rate': f"{(occupied_rooms / total_rooms * 100):.1f}%" if total_rooms > 0 else "0%"
            },
            'clients': {
                'total': total_clients,
                'current': current_clients,
                'checked_out': total_clients - current_clients
            },
            'employees': {
                'total': total_employees,
                'active': active_employees,
                'inactive': total_employees - active_employees
            },
            'timestamp': timezone.now().isoformat()
        }

        return Response(statistics)


class ClientStatisticsView(APIView):
    """Статистика по клиентам"""

    def get(self, request):
        # Клиенты по городам
        clients_by_city = Client.objects.values('city').annotate(
            count=Count('id')
        ).order_by('-count')

        # Клиенты по типам номеров
        clients_by_room_type = Client.objects.values('room__room_type').annotate(
            count=Count('id')
        ).order_by('-count')

        # Среднее время проживания
        checked_out_clients = Client.objects.filter(check_out_date__isnull=False)
        avg_stay_days = 0
        if checked_out_clients.exists():
            total_days = sum([
                (client.check_out_date - client.check_in_date).days
                for client in checked_out_clients
            ])
            avg_stay_days = total_days / checked_out_clients.count()

        statistics = {
            'by_city': list(clients_by_city),
            'by_room_type': list(clients_by_room_type),
            'average_stay_days': round(avg_stay_days, 1),
            'current_clients': Client.objects.filter(check_out_date__isnull=True).count()
        }

        return Response(statistics)


class EmployeeScheduleView(APIView):
    """Управление расписанием сотрудников"""

    def get(self, request):
        employee_id = request.query_params.get('employee_id')

        if employee_id:
            try:
                employee = Employee.objects.get(id=employee_id)
                schedules = CleaningSchedule.objects.filter(employee=employee)

                schedule_data = []
                for schedule in schedules:
                    schedule_data.append({
                        'id': schedule.id,
                        'employee_id': employee.id,
                        'employee_name': str(employee),
                        'floor': schedule.floor,
                        'day_of_week': schedule.get_day_of_week_display(),
                        'day_code': schedule.day_of_week
                    })

                return Response({
                    'employee': {
                        'id': employee.id,
                        'name': str(employee),
                        'is_active': employee.is_active
                    },
                    'schedules': schedule_data
                })
            except Employee.DoesNotExist:
                return Response(
                    {'error': 'Сотрудник не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Все расписания
        schedules = CleaningSchedule.objects.all().select_related('employee')

        result = {}
        for schedule in schedules:
            employee_name = str(schedule.employee)
            if employee_name not in result:
                result[employee_name] = []

            result[employee_name].append({
                'floor': schedule.floor,
                'day': schedule.get_day_of_week_display()
            })

        return Response(result)

    def post(self, request):
        """Изменить расписание"""
        employee_id = request.data.get('employee_id')
        floor = request.data.get('floor')
        day_of_week = request.data.get('day_of_week')
        action = request.data.get('action')  # 'add' или 'remove'

        if not all([employee_id, floor, day_of_week, action]):
            return Response(
                {'error': 'Необходимы employee_id, floor, day_of_week, action'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employee = Employee.objects.get(id=employee_id)

            if action == 'add':
                schedule, created = CleaningSchedule.objects.get_or_create(
                    employee=employee,
                    floor=floor,
                    day_of_week=day_of_week
                )
                message = 'расписание добавлено' if created else 'расписание уже существует'

                return Response({
                    'status': message,
                    'schedule_id': schedule.id
                })

            elif action == 'remove':
                deleted_count, _ = CleaningSchedule.objects.filter(
                    employee=employee,
                    floor=floor,
                    day_of_week=day_of_week
                ).delete()

                if deleted_count > 0:
                    return Response({'status': 'расписание удалено'})
                else:
                    return Response({'status': 'расписание не найдено'})

            else:
                return Response(
                    {'error': 'Действие должно быть "add" или "remove"'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Employee.DoesNotExist:
            return Response(
                {'error': 'Сотрудник не найден'},
                status=status.HTTP_404_NOT_FOUND
            )