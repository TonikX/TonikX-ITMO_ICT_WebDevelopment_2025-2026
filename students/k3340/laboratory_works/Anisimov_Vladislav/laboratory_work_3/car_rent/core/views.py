from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import generics, viewsets
from django.db.models import Count, Max, Sum, F, Q
from django.db.models.functions import Concat
from .models import *
from .serializers import *
from rest_framework import status

class CarInfoAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarInfoSerializer
    queryset = CarInfo.objects.all()

class CarAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

class CarInstanceAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarInstanceSerializer
    queryset = CarInstance.objects.all()

class FineAPIViewSet(viewsets.ModelViewSet):
    serializer_class = FineSerializer
    queryset = Fine.objects.all()

class CarCrashAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarCrashSerializer
    queryset = CarCrash.objects.all()

class ClientAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

class WorkerAPIViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    def destroy(self, request, *args, **kwargs):
        if (request.user.is_superuser):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

class RentContractAPIViewSet(viewsets.ModelViewSet):
    serializer_class = RentContractSerializer
    queryset = RentContract.objects.all()

class UserListAPIViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class TimesRentedAPIView(APIView):
    def get(self, request):
        annotated = CarInstance.objects.annotate(count=Count('contracts'))
        return Response(dict([(car_instance.__str__(), car_instance.count) for car_instance in annotated]))

class DaysRentedAPIView(APIView):
    def get(self, request):
        annotated = CarInstance.objects.annotate(date=Sum(F('contracts__return_date') - F('contracts__start_date')))
        return Response(dict([(car_instance.__str__(), car_instance.date.days) for car_instance in annotated]))

class ProfitByCarAPIView(APIView):
    def get(self, request):
        annotated = CarInstance.objects.annotate(date=Sum(F('contracts__return_date') - F('contracts__start_date')))
        return Response(dict([(car_instance.__str__(), car_instance.date.days * car_instance.price) for car_instance in annotated]))

class FinesByClientAPIView(APIView):
    def get(self, request):
        annotated = Fine.objects.annotate(client=F("car_instance__contracts__client"),
                                          name=Concat("car_instance__contracts__client__user__first_name",  
                                                      models.Value(' '), 
                                                      "car_instance__contracts__client__user__last_name"),
                                          start=F("car_instance__contracts__start_date"), 
                                          end=F("car_instance__contracts__return_date")).filter(start__lt=F('date'), end__gt=F('date'))

        return Response(dict([(client['name'], client['count']) for client in annotated.values("client").annotate(count=Count('client'), name=F('name'))]))