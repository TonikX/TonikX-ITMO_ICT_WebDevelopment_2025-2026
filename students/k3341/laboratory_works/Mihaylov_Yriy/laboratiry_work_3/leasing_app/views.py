from datetime import date

from django.db.models import IntegerField, Count
from django.db.models import (
    Sum, F, FloatField,
    ExpressionWrapper, Case, When
)
from django.db.models.functions import ExtractDay
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Car, CarSpecification, MaintenanceCompany, Maintenance,
    LeaseApplication, Lease, Client, Fleet, CarFleet
)
from .serializers import (
    CarSerializer, CarDetailSerializer, CarSpecificationSerializer,
    MaintenanceCompanySerializer, MaintenanceSerializer,
    LeaseApplicationSerializer, PublicLeaseApplicationSerializer,
    LeaseSerializer, LeaseStatusUpdateSerializer, ClientSerializer, FleetSerializer, CarFleetSerializer
)


# ------------------------ ADMIN CARS ------------------------

class AdminCarListAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CarSerializer

    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response({"cars": serializer.data})


class AdminCarCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.save()
        return Response(
            {"success": f"Car '{car.id}' created successfully."},
            status=status.HTTP_201_CREATED
        )


class AdminCarDetailAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CarDetailSerializer

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarDetailSerializer(car)
        return Response({"car": serializer.data})

    def patch(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_car = serializer.save()
        return Response({"success": f"Car '{updated_car.id}' updated successfully."})

    def delete(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return Response(
            {"success": f"Car '{pk}' deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class CarSpecificationCreateAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CarSpecificationSerializer

    def post(self, request, id):
        try:
            car = Car.objects.get(id=id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        if hasattr(car, "specification"):
            return Response({"error": "Specification already exists"}, status=400)

        serializer = CarSpecificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        spec = serializer.save(car=car)

        return Response({
            "success": "Specification created",
            "specification": CarSpecificationSerializer(spec).data
        })


# ------------------------ MAINTENANCE COMPANIES ------------------------

class MaintenanceCompanyListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MaintenanceCompanySerializer

    def get(self, request):
        companies = MaintenanceCompany.objects.all()
        serializer = MaintenanceCompanySerializer(companies, many=True)
        return Response({"maintenance_companies": serializer.data})

    def post(self, request):
        serializer = MaintenanceCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()

        return Response(
            {"success": f"Компания '{company.name}' создана успешно."},
            status=status.HTTP_201_CREATED
        )


class MaintenanceCompanyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MaintenanceCompanySerializer

    def get_object(self, id):
        return get_object_or_404(MaintenanceCompany, id=id)

    def get(self, request, id):
        company = self.get_object(id)
        serializer = MaintenanceCompanySerializer(company)
        return Response({"company": serializer.data})

    def patch(self, request, id):
        company = self.get_object(id)
        serializer = MaintenanceCompanySerializer(
            company, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Компания обновлена успешно."})

    def delete(self, request, id):
        company = self.get_object(id)
        company.delete()
        return Response({"success": "Компания удалена."})


# ------------------------ MAINTENANCE ------------------------

class CarMaintenanceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MaintenanceSerializer

    def get(self, request, id):
        car = get_object_or_404(Car, id=id)
        maintenances = Maintenance.objects.filter(car=car)
        serializer = MaintenanceSerializer(maintenances, many=True)
        return Response({"maintenances": serializer.data})

    def post(self, request, id):
        car = get_object_or_404(Car, id=id)

        data = request.data
        data["car"] = car.id
        data["created_by_admin"] = request.user.id

        serializer = MaintenanceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"success": f"Обслуживание добавлено для автомобиля {car.id}."},
            status=status.HTTP_201_CREATED
        )


# ------------------------ LEASE APPLICATIONS ------------------------

class LeaseApplicationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = LeaseApplicationSerializer

    def get(self, request, id=None):
        if id is None:
            apps = LeaseApplication.objects.all().order_by("-created_at")
            serializer = LeaseApplicationSerializer(apps, many=True)
            return Response({"applications": serializer.data})

        app = get_object_or_404(LeaseApplication, id=id)
        serializer = LeaseApplicationSerializer(app)
        return Response({"application": serializer.data})

    def post(self, request, id):
        if not request.path.endswith("/approve/"):
            return Response(
                {"error": "Используйте /approve/ для подтверждения заявки"},
                status=status.HTTP_400_BAD_REQUEST
            )

        app = get_object_or_404(LeaseApplication, id=id)

        lease = Lease.objects.create(
            car=app.car,
            client=app.client,
            start_date=request.data.get("start_date"),
            end_date=request.data.get("end_date"),
            monthly_payment=request.data.get("monthly_payment"),
            status="active",
            created_by_admin=request.user
        )

        # {"end_date": "2025-12-12",
        #  "start_date": "2025-12-11",
        #  "monthly_payment": 10
        #  }

        app.car.status = "leased"
        app.car.save()

        app.delete()

        return Response(
            {"success": f"Заявка подтверждена. Договор #{lease.id} создан."},
            status=status.HTTP_201_CREATED
        )


# ------------------------ LEASES ------------------------

class LeaseAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = LeaseSerializer

    def get(self, request):
        leases = Lease.objects.all()
        serializer = LeaseSerializer(leases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        car_id = request.data.get("car_id")
        client_id = request.data.get("client_id")

        if not car_id or not client_id:
            return Response(
                {"error": "car_id и client_id обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            car = Car.objects.get(id=car_id)
            client = Client.objects.get(id=client_id)
        except (Car.DoesNotExist, Client.DoesNotExist):
            return Response(
                {"error": "Car или Client не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        lease = Lease.objects.create(
            car=car,
            client=client,
            start_date=request.data.get("start_date"),
            end_date=request.data.get("end_date"),
            monthly_payment=request.data.get("monthly_payment"),
            status="active",
            created_by_admin=request.user,
        )

        serializer = LeaseSerializer(lease)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        """Обновление статуса аренды"""
        lease_id = request.data.get("lease_id")
        new_status = request.data.get("status")
        end_date = request.data.get("end_date")
        start_date = request.data.get("start_date")
        monthly_payment = request.data.get("monthly_payment")

        if not lease_id or not new_status:
            return Response(
                {"error": "lease_id и status обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lease = Lease.objects.get(id=lease_id)
        except Lease.DoesNotExist:
            return Response(
                {"error": "Lease не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeaseStatusUpdateSerializer(lease, data={
            "status": new_status,
            "start_date": start_date,
            "end_date": end_date,
            "monthly_payment": monthly_payment}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"success": "Статус обновлен"}, status=status.HTTP_200_OK)



# ------------------------ CLIENTS ------------------------

class ClientAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ClientSerializer

    def get(self, request, id=None):
        if id is None:
            clients = Client.objects.all().order_by("-created_at")
            serializer = ClientSerializer(clients, many=True)
            return Response({"clients": serializer.data})

        client = get_object_or_404(Client, id=id)
        serializer = ClientSerializer(client)
        return Response({"client": serializer.data})


# ------------------------ PUBLIC (CLIENT SIDE) ------------------------

class CarsListAPIView(APIView):
    serializer_class = CarSerializer

    def get(self, request):
        cars = Car.objects.filter(status="available").order_by("id")
        serializer = CarSerializer(cars, many=True)
        return Response({"cars": serializer.data})


class CarDetailAPIView(APIView):
    serializer_class = CarSerializer

    def get(self, request, id):
        car = get_object_or_404(Car, id=id)
        serializer = CarSerializer(car)
        return Response({"car": serializer.data})


class CarApplicationAPIView(APIView):
    serializer_class = PublicLeaseApplicationSerializer

    def post(self, request, id):
        car = get_object_or_404(Car, id=id)

        if car.status != "available":
            return Response(
                {"error": "Автомобиль в данный момент недоступен для бронирования."},
                status=status.HTTP_400_BAD_REQUEST
            )

        public_serializer = PublicLeaseApplicationSerializer(data=request.data)
        public_serializer.is_valid(raise_exception=True)
        validated = public_serializer.validated_data

        company_name = validated["company_name"].strip()
        inn = validated["inn"].strip()

        client_qs = Client.objects.filter(company_name=company_name, inn=inn)
        if client_qs.exists():
            client = client_qs.first()
            created_new_client = False
        else:
            client_serializer = ClientSerializer(data=validated)
            client_serializer.is_valid(raise_exception=True)
            client = client_serializer.save()
            created_new_client = True

        lease_app = LeaseApplication.objects.create(
            car=car,
            client=client
        )

        app_serializer = LeaseApplicationSerializer(lease_app)

        return Response(
            {
                "success": "Заявка создана.",
                "application": app_serializer.data,
                "client_created": created_new_client
            },
            status=status.HTTP_201_CREATED
        )


class AdminCarSpecificationAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CarSpecificationSerializer

    def get(self, request):
        specs = CarSpecification.objects.all()
        serializer = CarSpecificationSerializer(specs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSpecificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # car указать обязан
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        spec_id = request.data.get("id")
        if not spec_id:
            return Response({"error": "id обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            spec = CarSpecification.objects.get(id=spec_id)
        except CarSpecification.DoesNotExist:
            return Response({"error": "CarSpecification не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CarSpecificationSerializer(spec, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        spec_id = request.data.get("id")
        if not spec_id:
            return Response({"error": "id обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            spec = CarSpecification.objects.get(id=spec_id)
        except CarSpecification.DoesNotExist:
            return Response({"error": "CarSpecification не найден"}, status=status.HTTP_404_NOT_FOUND)

        spec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminFleetAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = FleetSerializer

    def get(self, request):
        fleets = Fleet.objects.all()
        serializer = FleetSerializer(fleets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FleetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        fleet_id = request.data.get("id")
        if not fleet_id:
            return Response({"error": "id обязателен"}, status=400)

        try:
            fleet = Fleet.objects.get(id=fleet_id)
        except Fleet.DoesNotExist:
            return Response({"error": "Fleet не найден"}, status=404)

        serializer = FleetSerializer(fleet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        fleet_id = request.data.get("id")
        if not fleet_id:
            return Response({"error": "id обязателен"}, status=400)

        try:
            fleet = Fleet.objects.get(id=fleet_id)
        except Fleet.DoesNotExist:
            return Response({"error": "Fleet не найден"}, status=404)

        fleet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminCarFleetAPIView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CarFleetSerializer

    def get(self, request):
        carfleets = CarFleet.objects.all()
        serializer = CarFleetSerializer(carfleets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarFleetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        cf_id = request.data.get("id")
        if not cf_id:
            return Response({"error": "id обязателен"}, status=400)

        try:
            carfleet = CarFleet.objects.get(id=cf_id)
        except CarFleet.DoesNotExist:
            return Response({"error": "CarFleet не найден"}, status=404)

        serializer = CarFleetSerializer(carfleet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        cf_id = request.data.get("id")
        if not cf_id:
            return Response({"error": "id обязателен"}, status=400)

        try:
            carfleet = CarFleet.objects.get(id=cf_id)
        except CarFleet.DoesNotExist:
            return Response({"error": "CarFleet не найден"}, status=404)

        carfleet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarLeasingsListAPIView(APIView):
    serializer_class = LeaseSerializer

    def get(self, request, id):
        car = get_object_or_404(Car, id=id)
        leasings = Lease.objects.filter(car=car).order_by("id")
        serializer = self.serializer_class(leasings, many=True)
        return Response({"leasings": serializer.data})



class CarSpecificationsListAPIView(APIView):
    serializer_class = CarSpecificationSerializer

    def get(self, request, id):
        car = get_object_or_404(Car, id=id)
        specs = CarSpecification.objects.filter(car=car).order_by("id")
        serializer = self.serializer_class(specs, many=True)
        return Response({"specifications": serializer.data})



class CarSpecificationCreateAPIView2(APIView):
    serializer_class = CarSpecificationSerializer

    def post(self, request, id):
        car = get_object_or_404(Car, id=id)

        data = request.data.copy()
        data["car"] = car.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"specification": serializer.data}, status=201)

        return Response(serializer.errors, status=400)


class CarLeasingStatsAPIView(APIView):
    """ отчет по доходам от каждого авто """
    def get(self, request):
        qs = (
            Car.objects
            .annotate(
                leasings_count=Count("leases"),
                total_income=Sum("leases__monthly_payment")
            )
            .values("make", "model", "leasings_count", "total_income")
        )
        return Response({"results": list(qs)})


class CarUtilizationAPIView(APIView):
    """ отчет по использованию авто """
    def get(self, request):
        cars = Car.objects.all().prefetch_related("leases")

        results = []
        today = date.today()

        for car in cars:
            total_days = (today - (car.purchase_date or today)).days or 1

            lease_days = 0
            for lease in car.leases.all():
                start = lease.start_date
                end = lease.end_date or today
                lease_days += (end - start).days

            utilization = round(lease_days / total_days, 3)/365 if total_days > 0 else None

            results.append({
                "make": car.make,
                "model": car.model,
                "license_plate": car.license_plate,
                "lease_days": lease_days,
                "utilization": utilization
            })

        return Response({"results": results})


class MaintenanceCostReportAPIView(APIView):
    """отчет по тратам на обслуживание для каждого авто"""
    def get(self, request):
        qs = Maintenance.objects.values(
            "car__id",
            "car__make",
            "car__model"
        ).annotate(
            total_cost=Sum("cost")
        ).order_by("car__id")

        results = []
        for item in qs:
            results.append({
                "car_id": item["car__id"],
                "car": f"{item['car__make']} {item['car__model']}",
                "total_maintenance_cost": item["total_cost"] or 0
            })

        return Response({"results": results})

