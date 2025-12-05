from rest_framework import viewsets, filters, status
from .models import Patient, Doctor, DoctorSchedule, Room, MedicalRecord, Visit, Payment
from .serializers import PatientSerializer, DoctorSerializer, DoctorScheduleSerializer, RoomSerializer, MedicalRecordSerializer, VisitSerializer, PaymentSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('last_name')
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['last_name','first_name','phone']
    ordering_fields = ['last_name','birth_date']

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related('doctor','record__patient','room').all()
    serializer_class = VisitSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('visit__record__patient').all()
    serializer_class = PaymentSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer

