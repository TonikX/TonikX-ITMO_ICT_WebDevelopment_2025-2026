from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Newspaper, PrintingHouse, PostOffice, PrintingRun, Distribution
)
from .serializers import (
    NewspaperSerializer, PrintingHouseSerializer, PostOfficeSerializer, DistributionSerializer,
    PrintingHouseDetailSerializer, PostOfficeDetailSerializer, NewspaperDetailSerializer
)


class NewspaperViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с газетами"""
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создание новой газеты"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Полное обновление газеты"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление газеты"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление газеты"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Газета успешно удалена'},
            status=status.HTTP_204_NO_CONTENT
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

    @action(detail=True, methods=['get'])
    def full_detail(self, request, pk=None):
        """GET-запрос для газеты с вложенными объектами (many-to-many)
        Возвращает газету с вложенными тиражами и распределениями"""
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
    """ViewSet для работы с типографиями"""
    queryset = PrintingHouse.objects.all()
    serializer_class = PrintingHouseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создание новой типографии"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Полное обновление типографии"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление типографии"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление типографии"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Типография успешно удалена'},
            status=status.HTTP_204_NO_CONTENT
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
    """ViewSet для работы с почтовыми отделениями"""
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создание нового почтового отделения"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Полное обновление почтового отделения"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление почтового отделения"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление почтового отделения"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Почтовое отделение успешно удалено'},
            status=status.HTTP_204_NO_CONTENT
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
    """ViewSet для работы с распределениями"""
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создание нового распределения"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Полное обновление распределения"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление распределения"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление распределения"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Распределение успешно удалено'},
            status=status.HTTP_204_NO_CONTENT
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
