from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Max, Sum, Count
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    Newspaper, PrintingHouse, PostOffice, PrintingRun, Distribution
)
from .serializers import (
    NewspaperSerializer, PrintingHouseSerializer, PostOfficeSerializer,
    PrintingRunSerializer, DistributionSerializer,
    PrintingHouseDetailSerializer, PostOfficeDetailSerializer, NewspaperDetailSerializer
)


class NewspaperViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с газетами
    
    Требует аутентификации через Token или Session.
    """
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'full_detail':
            return NewspaperDetailSerializer
        return NewspaperSerializer

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Название газеты (частичное совпадение)",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response('Список адресов типографий, где печатается газета'),
            400: openapi.Response('Ошибка: параметр name обязателен'),
            404: openapi.Response('Газета не найдена'),
            401: openapi.Response('Требуется аутентификация'),
        },
        operation_summary="Поиск адресов типографий по названию газеты",
        operation_description="Возвращает список адресов типографий, где печатаются газеты с указанным наименованием",
        security=[{'Token': []}, {'Session': []}]
    )
    @action(detail=False, methods=['get'])
    def by_name(self, request):
        """По каким адресам печатаются газеты данного наименования?"""
        newspaper_name = request.query_params.get('name', None)
        if not newspaper_name:
            return Response(
                {'error': 'Параметр name обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        newspapers = Newspaper.objects.filter(title__icontains=newspaper_name)
        if not newspapers.exists():
            return Response(
                {'error': f'Газета "{newspaper_name}" не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        result = []
        for newspaper in newspapers:
            printing_runs = PrintingRun.objects.filter(newspaper=newspaper)
            addresses = [
                {
                    'printing_house': run.printing_house.name,
                    'address': run.printing_house.address,
                    'circulation': run.circulation
                }
                for run in printing_runs
            ]
            result.append({
                'newspaper': NewspaperSerializer(newspaper).data,
                'printing_addresses': addresses
            })
        
        return Response(result)

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="ID газеты",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Название газеты (точное совпадение)",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={
            200: openapi.Response('Информация о газете'),
            400: openapi.Response('Ошибка: необходимо указать id или name'),
            404: openapi.Response('Газета не найдена'),
        },
        operation_summary="Получить информацию о газете",
        operation_description="Возвращает индекс и цену указанной газеты по ID или названию"
    )
    @action(detail=False, methods=['get'])
    def info(self, request):
        """Справка об индексе и цене указанной газеты"""
        newspaper_id = request.query_params.get('id', None)
        newspaper_name = request.query_params.get('name', None)
        
        if newspaper_id:
            try:
                newspaper = Newspaper.objects.get(id=newspaper_id)
            except Newspaper.DoesNotExist:
                return Response(
                    {'error': 'Газета не найдена'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif newspaper_name:
            try:
                newspaper = Newspaper.objects.get(title__iexact=newspaper_name)
            except Newspaper.DoesNotExist:
                return Response(
                    {'error': 'Газета не найдена'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Необходимо указать id или name газеты'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'title': newspaper.title,
            'publication_index': newspaper.publication_index,
            'price_per_copy': str(newspaper.price_per_copy),
            'editor': newspaper.editor_full_name
        })

    @swagger_auto_schema(
        method='get',
        responses={
            200: NewspaperDetailSerializer,
            404: openapi.Response('Газета не найдена'),
        },
        operation_summary="Получить детальную информацию о газете",
        operation_description="Возвращает газету с вложенными тиражами и распределениями (many-to-many через промежуточные модели)"
    )
    @action(detail=True, methods=['get'])
    def full_detail(self, request, pk=None):
        """GET-запрос для газеты с вложенными объектами (many-to-many)
        Возвращает газету с вложенными тиражами и распределениями,
        что демонстрирует связь many-to-many через промежуточные модели"""
        try:
            newspaper = Newspaper.objects.prefetch_related(
                'printingrun_set',
                'distribution_set'
            ).get(pk=pk)
        except Newspaper.DoesNotExist:
            return Response(
                {'error': 'Газета не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = NewspaperDetailSerializer(newspaper)
        return Response(serializer.data)


class PrintingHouseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с типографиями
    
    Требует аутентификации через Token или Session.
    """
    queryset = PrintingHouse.objects.all()
    serializer_class = PrintingHouseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'full_detail':
            return PrintingHouseDetailSerializer
        return PrintingHouseSerializer

    @swagger_auto_schema(
        method='get',
        responses={
            200: openapi.Response('Информация о редакторе газеты с наибольшим тиражом'),
            404: openapi.Response('Типография не найдена или в ней не печатаются газеты'),
        },
        operation_summary="Редактор газеты с наибольшим тиражом",
        operation_description="Возвращает фамилию редактора газеты, которая печатается в указанной типографии самым большим тиражом"
    )
    @action(detail=True, methods=['get'])
    def largest_circulation_editor(self, request, pk=None):
        """Фамилия редактора газеты, которая печатается в указанной типографии самым большим тиражом"""
        try:
            printing_house = PrintingHouse.objects.get(pk=pk)
        except PrintingHouse.DoesNotExist:
            return Response(
                {'error': 'Типография не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        largest_run = PrintingRun.objects.filter(
            printing_house=printing_house
        ).order_by('-circulation').first()
        
        if not largest_run:
            return Response(
                {'error': 'В данной типографии не печатаются газеты'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        newspaper = largest_run.newspaper
        return Response({
            'printing_house': printing_house.name,
            'newspaper': newspaper.title,
            'circulation': largest_run.circulation,
            'editor_last_name': newspaper.editor_last_name,
            'editor_full_name': newspaper.editor_full_name
        })

    @swagger_auto_schema(
        method='get',
        responses={
            200: PrintingHouseDetailSerializer,
            404: openapi.Response('Типография не найдена'),
        },
        operation_summary="Получить детальную информацию о типографии",
        operation_description="Возвращает типографию с вложенными тиражами газет (one-to-many)"
    )
    @action(detail=True, methods=['get'])
    def full_detail(self, request, pk=None):
        """GET-запрос для типографии с вложенными тиражами (one-to-many)
        Возвращает типографию с вложенными тиражами газет"""
        try:
            printing_house = PrintingHouse.objects.prefetch_related(
                'printingrun_set'
            ).get(pk=pk)
        except PrintingHouse.DoesNotExist:
            return Response(
                {'error': 'Типография не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PrintingHouseDetailSerializer(printing_house)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='get',
        responses={
            200: openapi.Response('Отчет о работе типографий'),
        },
        operation_summary="Отчет о работе типографий",
        operation_description="Возвращает отчет о работе активных типографий с почтовыми отделениями города"
    )
    @action(detail=False, methods=['get'])
    def report(self, request):
        """Отчет о работе типографий с почтовыми отделениями города"""
        printing_houses = PrintingHouse.objects.filter(is_active=True)
        
        result = []
        for ph in printing_houses:
            printing_runs = PrintingRun.objects.filter(printing_house=ph)
            total_newspapers = printing_runs.count()
            
            newspapers_detail = []
            for run in printing_runs:
                distributions = Distribution.objects.filter(
                    printing_house=ph,
                    newspaper=run.newspaper
                )
                
                post_offices_detail = []
                for dist in distributions:
                    post_offices_detail.append({
                        'post_office_number': dist.post_office.number,
                        'post_office_address': dist.post_office.address,
                        'quantity': dist.quantity
                    })
                
                newspapers_detail.append({
                    'newspaper': run.newspaper.title,
                    'circulation': run.circulation,
                    'distributions': post_offices_detail,
                    'total_distributed': sum(d.quantity for d in distributions)
                })
            
            result.append({
                'printing_house': PrintingHouseSerializer(ph).data,
                'total_newspapers': total_newspapers,
                'newspapers': newspapers_detail
            })
        
        return Response(result)


class PostOfficeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с почтовыми отделениями
    
    Требует аутентификации через Token или Session.
    """
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'full_detail':
            return PostOfficeDetailSerializer
        return PostOfficeSerializer

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'min_price',
                openapi.IN_QUERY,
                description="Минимальная цена газеты",
                type=openapi.TYPE_NUMBER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response('Список почтовых отделений с газетами дороже указанной цены'),
            400: openapi.Response('Ошибка: параметр min_price обязателен или неверный формат'),
        },
        operation_summary="Поиск почтовых отделений по минимальной цене газеты",
        operation_description="Возвращает список почтовых отделений, куда поступают газеты с ценой больше указанной"
    )
    @action(detail=False, methods=['get'])
    def by_price(self, request):
        """На какие почтовые отделения (адреса) поступает газета, имеющая цену, больше указанной"""
        min_price = request.query_params.get('min_price', None)
        if not min_price:
            return Response(
                {'error': 'Параметр min_price обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            min_price = float(min_price)
        except ValueError:
            return Response(
                {'error': 'min_price должен быть числом'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        newspapers = Newspaper.objects.filter(price_per_copy__gt=min_price)
        if not newspapers.exists():
            return Response([])
        
        post_offices = PostOffice.objects.filter(
            distribution__newspaper__in=newspapers
        ).distinct()
        
        result = []
        for po in post_offices:
            distributions = Distribution.objects.filter(
                post_office=po,
                newspaper__price_per_copy__gt=min_price
            ).select_related('newspaper')
            
            newspapers_list = [
                {
                    'title': dist.newspaper.title,
                    'price': str(dist.newspaper.price_per_copy),
                    'quantity': dist.quantity
                }
                for dist in distributions
            ]
            
            result.append({
                'post_office': PostOfficeSerializer(po).data,
                'newspapers': newspapers_list
            })
        
        return Response(result)

    @swagger_auto_schema(
        method='get',
        responses={
            200: PostOfficeDetailSerializer,
            404: openapi.Response('Почтовое отделение не найдено'),
        },
        operation_summary="Получить детальную информацию о почтовом отделении",
        operation_description="Возвращает почтовое отделение с вложенными распределениями газет (one-to-many)"
    )
    @action(detail=True, methods=['get'])
    def full_detail(self, request, pk=None):
        """GET-запрос для почтового отделения с вложенными распределениями (one-to-many)
        Возвращает почтовое отделение с вложенными распределениями газет"""
        try:
            post_office = PostOffice.objects.prefetch_related(
                'distribution_set'
            ).get(pk=pk)
        except PostOffice.DoesNotExist:
            return Response(
                {'error': 'Почтовое отделение не найдено'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PostOfficeDetailSerializer(post_office)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'max_quantity',
                openapi.IN_QUERY,
                description="Максимальное количество экземпляров",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response('Список газет с количеством меньше указанного'),
            400: openapi.Response('Ошибка: параметр max_quantity обязателен или неверный формат'),
        },
        operation_summary="Поиск газет с низким количеством",
        operation_description="Возвращает список газет и почтовых отделений, куда они поступают в количестве меньшем заданного"
    )
    @action(detail=False, methods=['get'])
    def low_quantity(self, request):
        """Какие газеты и куда (номер почты) поступают в количестве меньшем, чем заданное"""
        max_quantity = request.query_params.get('max_quantity', None)
        if not max_quantity:
            return Response(
                {'error': 'Параметр max_quantity обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            max_quantity = int(max_quantity)
        except ValueError:
            return Response(
                {'error': 'max_quantity должен быть целым числом'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        distributions = Distribution.objects.filter(quantity__lt=max_quantity)
        
        result = []
        for dist in distributions:
            result.append({
                'newspaper': NewspaperSerializer(dist.newspaper).data,
                'post_office_number': dist.post_office.number,
                'post_office_address': dist.post_office.address,
                'quantity': dist.quantity
            })
        
        return Response(result)


class DistributionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с распределениями
    
    Требует аутентификации через Token или Session.
    """
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'newspaper_id',
                openapi.IN_QUERY,
                description="ID газеты",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'newspaper_name',
                openapi.IN_QUERY,
                description="Название газеты (точное совпадение)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'address',
                openapi.IN_QUERY,
                description="Адрес типографии",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response('Список распределений газеты'),
            400: openapi.Response('Ошибка: необходимо указать newspaper_id или newspaper_name, address обязателен'),
            404: openapi.Response('Газета, типография или распределения не найдены'),
        },
        operation_summary="Поиск распределений по газете и адресу типографии",
        operation_description="Возвращает список почтовых отделений, куда поступает указанная газета, печатающаяся по указанному адресу"
    )
    @action(detail=False, methods=['get'])
    def by_newspaper_and_address(self, request):
        """Куда поступает данная газета, печатающаяся по данному адресу"""
        newspaper_id = request.query_params.get('newspaper_id', None)
        newspaper_name = request.query_params.get('newspaper_name', None)
        address = request.query_params.get('address', None)
        
        if not address:
            return Response(
                {'error': 'Параметр address обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Находим типографии по адресу
        printing_houses = PrintingHouse.objects.filter(address__icontains=address)
        if not printing_houses.exists():
            return Response(
                {'error': f'Типография по адресу "{address}" не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Находим газету
        if newspaper_id:
            try:
                newspaper = Newspaper.objects.get(id=newspaper_id)
            except Newspaper.DoesNotExist:
                return Response(
                    {'error': 'Газета не найдена'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif newspaper_name:
            try:
                newspaper = Newspaper.objects.get(title__iexact=newspaper_name)
            except Newspaper.DoesNotExist:
                return Response(
                    {'error': 'Газета не найдена'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Необходимо указать newspaper_id или newspaper_name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем, что газета печатается в этих типографиях
        printing_runs = PrintingRun.objects.filter(
            printing_house__in=printing_houses,
            newspaper=newspaper
        )
        if not printing_runs.exists():
            return Response(
                {'error': f'Газета "{newspaper.title}" не печатается по адресу "{address}"'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Находим распределения
        distributions = Distribution.objects.filter(
            printing_house__in=printing_houses,
            newspaper=newspaper
        )
        
        result = []
        for dist in distributions:
            result.append({
                'post_office': PostOfficeSerializer(dist.post_office).data,
                'quantity': dist.quantity,
                'printing_house': PrintingHouseSerializer(dist.printing_house).data
            })
        
        return Response({
            'newspaper': NewspaperSerializer(newspaper).data,
            'printing_address': address,
            'distributions': result
        })
