from django.db.models import Avg, Count, Sum, Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workshop, Cell, Employee, ResponsibleEmployee, Breed, Chicken, Diet, LaborContract
from .serializers import (
    EmployeeSerializer,
    ResponsibleEmployeeSerializer,
    DietSerializer, BreedSerializer, ChickenSerializer, LaborContractSerializer, CellSerializer,
    ResponsibleEmployeeWriteSerializer, BreedWriteSerializer, ChickenWriteSerializer, LaborContractWriteSerializer,
    CellWriteSerializer,
)


class EmployeeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class ResponsibleEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResponsibleEmployeeWriteSerializer

    def get(self, request):
        employees = ResponsibleEmployee.objects.all()
        serializer = ResponsibleEmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResponsibleEmployeeWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResponsibleEmployeeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResponsibleEmployeeWriteSerializer
    queryset = ResponsibleEmployee.objects.all()


class DietAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DietSerializer

    def get(self, request):
        diets = Diet.objects.all()
        serializer = DietSerializer(diets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DietSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DietDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DietSerializer
    queryset = Diet.objects.all()


class BreedAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BreedWriteSerializer

    def get(self, request):
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BreedWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BreedDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BreedWriteSerializer
    queryset = Breed.objects.all()


class ChickenAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChickenWriteSerializer

    def get(self, request):
        chickens = Chicken.objects.all()
        serializer = ChickenSerializer(chickens, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChickenWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChickenDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChickenWriteSerializer
    queryset = Chicken.objects.all()


class LaborContractsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LaborContractWriteSerializer

    def get(self, request):
        lab_contracts = LaborContract.objects.all()
        serializer = LaborContractSerializer(lab_contracts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LaborContractWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LaborContractDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LaborContractWriteSerializer
    queryset = LaborContract.objects.all()


class CellAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CellWriteSerializer

    def get(self, request):
        cells = Cell.objects.all()
        serializer = CellSerializer(cells, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CellWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EggPerformanceByWeightBreedAgeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Какое количество яиц получают от каждой курицы данного веса, породы, возраста?",
        manual_parameters=[
            openapi.Parameter(
                'weight',
                openapi.IN_QUERY,
                description="Вес",
                type=openapi.TYPE_NUMBER,
                required=True,
            ),
            openapi.Parameter(
                'age',
                openapi.IN_QUERY,
                description='Возраст',
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'breed_id',
                openapi.IN_QUERY,
                description='Идентификатор породы',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        weight = request.query_params.get("weight")
        breed_id = request.query_params.get("breed_id")
        age = request.query_params.get("age")

        chickens = Chicken.objects.filter(weight=weight, breed_id=breed_id, age=age)
        total_eggs = chickens.aggregate(Sum('egg_performance_month'))['egg_performance_month__sum'] or 0
        count = chickens.count()
        eggs_per_chicken = total_eggs / count if count > 0 else 0

        return Response({"eggs_per_chicken": eggs_per_chicken}, status=status.HTTP_200_OK)


class WorkshopWithMostBreedAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="В каком цехе наибольшее количество кур определенной породы?",
        manual_parameters=[
            openapi.Parameter(
                'breed_id',
                openapi.IN_QUERY,
                description="Идентификатор породы",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        breed_id = request.query_params.get("breed_id")
        workshop = Workshop.objects.annotate(
            breed_count=Count('cell__chicken', filter=Q(cell__chicken__breed_id=breed_id))
        ).order_by('-breed_count').first()

        return Response({
            "workshop": workshop.title if workshop else "No data",
            "breed_count": workshop.breed_count if workshop else 0
        }, status=status.HTTP_200_OK)


class AverageEggsPerEmployeeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Среднее количество яиц, которое получает в день каждый работник от обслуживаемых им кур? ",
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        employees = Employee.objects.annotate(
            total_eggs=Sum('responsibleemployee__cell__chicken__egg_performance_month'),
            chicken_count=Count('responsibleemployee__cell__chicken')
        ).filter(chicken_count__gt=0)

        data = [
            {
                "employee": f"{employee.first_name} {employee.second_name} {employee.patronymic}",
                "average_eggs_per_day": round(employee.total_eggs / 30, 2) if employee.total_eggs else 0
            }
            for employee in employees
        ]

        return Response(data, status=status.HTTP_200_OK)


class ChickenCountByBreedWorkshopAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Сколько кур каждой породы в каждом цехе?",
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        data = Cell.objects.values(
            'workshop__title', 'chicken__breed__name'
        ).annotate(chicken_count=Count('chicken'))

        response_data = [
            {
                "workshop": entry["workshop__title"],
                "breed_name": entry["chicken__breed__name"],
                "chicken_count": entry["chicken_count"],
            }
            for entry in data
        ]
        return Response(response_data, status=status.HTTP_200_OK)


class BreedPerformanceDifferenceAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Какова для каждой породы разница между показателями породы и средними показателями по птицефабрике? Из показателей породы вычитаются показатели по птицефабрике",
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        overall_avg = Chicken.objects.aggregate(
            avg_eggs=Avg('egg_performance_month'), avg_weight=Avg('weight')
        )

        breeds = Breed.objects.annotate(
            avg_eggs=Avg('chicken__egg_performance_month'),
            avg_weight=Avg('chicken__weight')
        ).values('name', 'avg_eggs', 'avg_weight')

        data = [
            {
                "breed": breed['name'],
                "egg_difference": int(breed['avg_eggs'] - overall_avg['avg_eggs']) if overall_avg['avg_eggs'] and breed[
                    'avg_eggs'] is not None else 0,
                "weight_difference": round(breed['avg_weight'] - overall_avg['avg_weight'], 2) if overall_avg[
                    'avg_weight'] and breed['avg_weight'] is not None else 0
            }
            for breed in breeds
        ]

        return Response(data, status=status.HTTP_200_OK)


class MonthlyReportAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_month_data = Chicken.objects.values('cell__workshop__title', 'breed__name').annotate(
            total_eggs=Sum('egg_performance_month'),
            chicken_count=Count('id'),
            avg_performance=Avg('egg_performance_month')
        )

        overall_stats = Chicken.objects.aggregate(
            total_chickens=Count('id'), total_eggs=Sum('egg_performance_month')
        )

        report = {
            "last_month_data": [
                {
                    "workshop": data['cell__workshop__title'],
                    "breed_name": data['breed__name'],
                    "chicken_count": data['chicken_count'],
                    "total_eggs": data['total_eggs'],
                    "avg_performance": data['avg_performance']
                }
                for data in last_month_data
            ],
            "overall_stats": overall_stats
        }

        return Response(report, status=status.HTTP_200_OK)
