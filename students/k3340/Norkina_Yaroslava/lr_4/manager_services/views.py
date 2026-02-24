import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Q, Avg
from .models import *
from .serializers import *
import os
from django.conf import settings
from django.core.files.storage import default_storage


class ServiceListAPIView(APIView):
    """
    GET: Список всех активных услуг (публичный)
    """

    def get(self, request):
        services = Service.objects.filter(is_active=True).order_by('-created_at')

        # Фильтрация по категории, если указана
        category = request.query_params.get('category')
        if category:
            services = services.filter(category=category)

        # Поиск по названию, если указан
        search = request.query_params.get('search')
        if search:
            services = services.filter(name__icontains=search)

        serializer = ServiceListSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)


class ServiceDetailAPIView(APIView):
    """
    GET: Детали услуги (публичный)
    """

    def get(self, request, pk):
        try:
            service = Service.objects.get(id=pk, is_active=True)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена или неактивна"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceDetailSerializer(service, context={'request': request})
        return Response(serializer.data)


class ServiceCategoriesAPIView(APIView):
    """
    GET: Список всех категорий услуг с количеством услуг в каждой
    """

    def get(self, request):
        # Получаем все категории из активных услуг
        categories = Service.objects.filter(is_active=True) \
            .values('category') \
            .annotate(service_count=Count('id')) \
            .order_by('category')

        # Преобразуем QuerySet в список словарей для сериализации
        categories_list = [
            {'name': cat['category'], 'service_count': cat['service_count']}
            for cat in categories
        ]

        serializer = CategorySerializer(categories_list, many=True)
        return Response(serializer.data)


class AdminServiceListAPIView(APIView):
    """
    GET: Список всех услуг (для админа, с неактивными)
    POST: Создание новой услуги (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ServiceAdminSerializer

    def get(self, request):
        services = Service.objects.all().order_by('-created_at')

        # Фильтрация по активности, если указана
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            services = services.filter(is_active=is_active.lower() == 'true')

        # Фильтрация по категории, если указана
        category = request.query_params.get('category')
        if category:
            services = services.filter(category=category)

        # Поиск по названию, если указан
        search = request.query_params.get('search')
        if search:
            services = services.filter(name__icontains=search)

        serializer = ServiceAdminSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceAdminSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminServiceDetailAPIView(APIView):
    """
    GET: Детали услуги (админ)
    PUT: Полное обновление услуги (админ)
    PATCH: Частичное обновление (админ)
    DELETE: Удаление услуги из БД (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ServiceAdminSerializer

    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return None

    def get(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceAdminSerializer(service, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceAdminSerializer(service, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceAdminSerializer(service, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, есть ли связанные заявки
        if service.orders.exists():
            return Response(
                {
                    "error": "Невозможно удалить услугу, так как существуют связанные заявки",
                    "order_count": service.orders.count()
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Удаляем файлы, связанные с услугой
        if service.files.exists():
            for file in service.files.all():

                file_path = os.path.join(settings.MEDIA_ROOT, file.file_path)


                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        # Логируем ошибку
                        print(f"Ошибка при удалении файла {file_path}: {e}")

                # Удаляем запись из БД
                file.delete()

        # Удаляем саму услугу
        service.delete()

        return Response(
            {"message": "Услуга успешно удалена"},
            status=status.HTTP_200_OK
        )


class AdminServiceDeactivateAPIView(APIView):
    """
    POST: Деактивация услуги (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Деактивируем услугу
        service.is_active = False
        service.save()

        serializer = ServiceAdminSerializer(service, context={'request': request})
        return Response({
            "message": "Услуга успешно деактивирована",
            "service": serializer.data
        })


class AdminFileUploadAPIView(APIView):
    """
    POST: Загрузка файла для услуги (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FileUploadSerializer

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем валидированные данные
        service = serializer.validated_data['service']
        uploaded_file = request.FILES['file']
        alt_text = serializer.validated_data.get('alt_text', '')
        is_primary = serializer.validated_data.get('is_primary', False)
        display_order = serializer.validated_data.get('display_order', 0)

        # Проверяем, что только один файл может быть главным
        if is_primary:
            existing_primary = File.objects.filter(service=service, is_primary=True).exists()
            if existing_primary:
                return Response(
                    {"error": "У услуги уже есть главное изображение"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Генерируем уникальное имя файла
        original_filename = uploaded_file.name
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Определяем путь для сохранения
        upload_path = f"services/{service.id}/{unique_filename}"

        # Сохраняем файл на диск
        file_path = default_storage.save(upload_path, uploaded_file)

        try:
            # Получаем информацию о файле
            file_size = uploaded_file.size
            mime_type = uploaded_file.content_type

            # Создаем запись в БД
            file_obj = File.objects.create(
                service=service,
                file_name=original_filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=mime_type,
                is_primary=is_primary,
                display_order=display_order,
                uploaded_by=request.user,
                alt_text=alt_text
            )

            # Сериализуем и возвращаем результат
            serializer = FileSerializer(file_obj, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Если что-то пошло не так, удаляем загруженный файл
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

            return Response(
                {"error": f"Ошибка при сохранении файла: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminFileDetailAPIView(APIView):
    """
    GET: Получить информацию о файле (админ)
    PUT: Обновить информацию о файле (админ)
    PATCH: Частичное обновление информации о файле (админ)
    DELETE: Удалить файл (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FileSerializer

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            return None

    def get(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FileSerializer(file_obj, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FileSerializer(file_obj, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что устанавливается is_primary
        if 'is_primary' in request.data and request.data['is_primary']:
            # Проверяем, есть ли уже главное изображение у этой услуги
            existing_primary = File.objects.filter(
                service=file_obj.service,
                is_primary=True
            ).exclude(id=file_obj.id).exists()

            if existing_primary:
                return Response(
                    {"error": "У услуги уже есть главное изображение"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = FileSerializer(file_obj, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Сохраняем путь к файлу перед удалением
        file_path = file_obj.file_path

        # Удаляем запись из БД
        file_obj.delete()

        # Удаляем физический файл с диска
        if default_storage.exists(file_path):
            try:
                default_storage.delete(file_path)
            except Exception as e:
                # Логируем ошибку, но не возвращаем ошибку пользователю
                print(f"Ошибка при удалении файла {file_path}: {e}")

        return Response(
            {"message": "Файл успешно удален"},
            status=status.HTTP_200_OK
        )


class ServiceFilesAPIView(APIView):
    """
    GET: Получить файлы для конкретной услуги (публичный)
    """

    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена или неактивна"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем файлы услуги, отсортированные по порядку отображения
        files = service.files.all().order_by('display_order', 'uploaded_at')

        file_type = request.query_params.get('type')
        if file_type == 'images':
            files = files.filter(mime_type__startswith='image/')
        elif file_type == 'documents':
            files = files.exclude(mime_type__startswith='image/')

        serializer = FileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data)


class OrderListCreateAPIView(APIView):
    """
    GET: Список заявок текущего пользователя
    POST: Создание новой заявки
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def get(self, request):
        # Получаем заявки текущего пользователя
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

        # Фильтрация по статусу, если указана
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)

        # Фильтрация по услуге, если указана
        service_id = request.query_params.get('service_id')
        if service_id:
            orders = orders.filter(service_id=service_id)

        serializer = OrderListSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Создаем заявку
        order = serializer.save()

        # Создаем запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            old_status='',  # Первый статус, поэтому старого нет
            new_status=order.status,
            changed_by=request.user,
            comment='Создание заявки'
        )

        # Возвращаем детали созданной заявки
        detail_serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    """
    GET: Детали заявки пользователя
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk, request.user)
        if not order:
            return Response(
                {"error": "Заявка не найдена или у вас нет к ней доступа"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(serializer.data)


class OrderCancelAPIView(APIView):
    """
    POST: Отмена заявки (пользователем)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена или у вас нет к ней доступа"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, можно ли отменить заявку
        if order.status == Order.Status.COMPLETED:
            return Response(
                {"error": "Нельзя отменить завершенную заявку"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == Order.Status.CANCELLED:
            return Response(
                {"error": "Заявка уже отменена"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Сохраняем старый статус
        old_status = order.status

        # Меняем статус на отменен
        order.status = Order.Status.CANCELLED
        order.save()

        # Создаем запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=order.status,
            changed_by=request.user,
            comment='Отмена пользователем'
        )

        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response({
            "message": "Заявка успешно отменена",
            "order": serializer.data
        })


class AdminOrderListAPIView(APIView):
    """
    GET: Список всех заявок (админ, с фильтрами)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')

        # Фильтрация по статусу
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)

        # Фильтрация по пользователю
        user_id = request.query_params.get('user_id')
        if user_id:
            orders = orders.filter(user_id=user_id)

        # Фильтрация по услуге
        service_id = request.query_params.get('service_id')
        if service_id:
            orders = orders.filter(service_id=service_id)

        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            orders = orders.filter(created_at__date__gte=date_from)

        # Фильтрация по дате создания (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            orders = orders.filter(created_at__date__lte=date_to)

        # Поиск по email пользователя
        search = request.query_params.get('search')
        if search:
            orders = orders.filter(
                Q(user__email__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(notes__icontains=search)
            )

        serializer = OrderAdminSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class AdminOrderDetailAPIView(APIView):
    """
    GET: Детали заявки (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderAdminSerializer(order, context={'request': request})
        return Response(serializer.data)


class AdminOrderStatusUpdateAPIView(APIView):
    """
    PATCH: Изменение статуса заявки (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrderStatusUpdateSerializer

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем старый статус
        old_status = order.status
        new_status = serializer.validated_data['status']
        comment = serializer.validated_data.get('comment', '')

        # Проверяем, что статус изменился
        if old_status == new_status:
            return Response(
                {"error": "Новый статус совпадает со старым"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что нельзя изменить статус завершенной заявки
        if old_status == Order.Status.COMPLETED:
            return Response(
                {"error": "Нельзя изменить статус завершенной заявки"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Меняем статус
        order.status = new_status
        order.save()

        # Создаем запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user,
            comment=comment or f'Изменение статуса администратором'
        )

        # Возвращаем обновленную заявку
        order_serializer = OrderAdminSerializer(order, context={'request': request})
        return Response({
            "message": "Статус заявки успешно обновлен",
            "order": order_serializer.data
        })


class AdminOrderHistoryAPIView(APIView):
    """
    GET: История статусов заявки (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем историю статусов для этой заявки
        history = order.status_history.all().order_by('-changed_at')

        serializer = OrderStatusHistorySerializer(history, many=True)
        return Response(serializer.data)


class OrderCommentsAPIView(APIView):
    """
    GET: Получить комментарии к заявке (видимые пользователю)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            # Проверяем, что заявка принадлежит пользователю или пользователь - админ
            if request.user.is_admin:
                order = Order.objects.get(pk=order_id)
            else:
                order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена или у вас нет к ней доступа"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем только видимые комментарии
        comments = order.comments.filter(is_visible_to_user=True).order_by('created_at')

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)


class AdminCommentListAPIView(APIView):
    """
    GET: Список всех комментариев (админ, с фильтрами)
    POST: Добавить комментарий к заявке (админ)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.all().order_by('-created_at')

        # Фильтрация по заявке
        order_id = request.query_params.get('order_id')
        if order_id:
            comments = comments.filter(order_id=order_id)

        # Фильтрация по администратору
        admin_id = request.query_params.get('admin_id')
        if admin_id:
            comments = comments.filter(admin_id=admin_id)

        # Фильтрация по видимости
        is_visible = request.query_params.get('is_visible')
        if is_visible is not None:
            comments = comments.filter(is_visible_to_user=is_visible.lower() == 'true')

        # Поиск по содержимому
        search = request.query_params.get('search')
        if search:
            comments = comments.filter(content__icontains=search)

        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            comments = comments.filter(created_at__date__gte=date_from)

        # Фильтрация по дате создания (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            comments = comments.filter(created_at__date__lte=date_to)

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Проверяем, что заявка существует
        order_id = request.data.get('order')
        if not order_id:
            return Response(
                {"error": "Не указана заявка"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Создаем комментарий
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminCommentDetailAPIView(APIView):
    """
    GET: Получить комментарий (админ)
    PUT: Обновить комментарий (админ)
    PATCH: Частичное обновление комментария (админ)
    DELETE: Удалить комментарий (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CommentSerializer

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что можно редактировать только свои комментарии
        if comment.admin != request.user:
            return Response(
                {"error": "Вы можете редактировать только свои комментарии"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Для изменения видимости - доступно всем админам
        # Для изменения контента - только автору
        if 'content' in request.data and comment.admin != request.user:
            return Response(
                {"error": "Вы можете редактировать только свои комментарии"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что можно удалять только свои комментарии
        if comment.admin != request.user:
            return Response(
                {"error": "Вы можете удалять только свои комментарии"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(
            {"message": "Комментарий успешно удален"},
            status=status.HTTP_200_OK
        )


class AdminCommentVisibilityAPIView(APIView):
    """
    PATCH: Изменить видимость комментария (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentVisibilitySerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Видимость комментария успешно изменена",
            "comment": CommentSerializer(comment, context={'request': request}).data
        })


class ServiceReviewsAPIView(APIView):
    """
    GET: Список опубликованных отзывов на услугу
    """

    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена или неактивна"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем только опубликованные отзывы
        reviews = service.reviews.filter(is_published=True).order_by('-created_at')

        # Фильтрация по рейтингу, если указан
        rating = request.query_params.get('rating')
        if rating:
            reviews = reviews.filter(rating=rating)

        # Фильтрация по подтвержденным отзывам
        verified_only = request.query_params.get('verified_only')
        if verified_only and verified_only.lower() == 'true':
            reviews = reviews.filter(is_verified=True)

        # Пагинация (базовая)
        limit = request.query_params.get('limit')
        if limit and limit.isdigit():
            reviews = reviews[:int(limit)]

        # Статистика по отзывам
        total_reviews = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        rating_distribution = reviews.values('rating').annotate(count=Count('id')).order_by('-rating')

        serializer = ReviewListSerializer(reviews, many=True, context={'request': request})

        return Response({
            "service_id": service_id,
            "service_name": service.name,
            "statistics": {
                "total_reviews": total_reviews,
                "average_rating": round(average_rating, 1),
                "rating_distribution": list(rating_distribution)
            },
            "reviews": serializer.data
        })


class UserReviewCreateAPIView(APIView):
    """
    POST: Создать отзыв (только для завершенных заказов пользователя)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        review = serializer.save()

        # Возвращаем детали созданного отзыва
        detail_serializer = ReviewDetailSerializer(review, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(APIView):
    """
    GET: Детали отзыва (публичный)
    """

    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk, is_published=True)
        except Review.DoesNotExist:
            return Response(
                {"error": "Отзыв не найден или не опубликован"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewDetailSerializer(review, context={'request': request})
        return Response(serializer.data)


class AdminReviewListAPIView(APIView):
    """
    GET: Все отзывы (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        reviews = Review.objects.all().order_by('-created_at')

        # Фильтрация по услуге
        service_id = request.query_params.get('service_id')
        if service_id:
            reviews = reviews.filter(service_id=service_id)

        # Фильтрация по пользователю
        user_id = request.query_params.get('user_id')
        if user_id:
            reviews = reviews.filter(user_id=user_id)

        # Фильтрация по статусу публикации
        is_published = request.query_params.get('is_published')
        if is_published is not None:
            reviews = reviews.filter(is_published=is_published.lower() == 'true')

        # Фильтрация по подтверждению
        is_verified = request.query_params.get('is_verified')
        if is_verified is not None:
            reviews = reviews.filter(is_verified=is_verified.lower() == 'true')

        # Фильтрация по рейтингу
        rating = request.query_params.get('rating')
        if rating:
            reviews = reviews.filter(rating=rating)


        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            reviews = reviews.filter(created_at__date__gte=date_from)

        # Фильтрация по дате создания (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            reviews = reviews.filter(created_at__date__lte=date_to)

        serializer = ReviewAdminSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)


class AdminPendingReviewsAPIView(APIView):
    """
    GET: Список отзывов на модерации (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Отзывы, ожидающие модерации (не опубликованные)
        pending_reviews = Review.objects.filter(is_published=False).order_by('created_at')

        # Фильтрация по услуге, если указана
        service_id = request.query_params.get('service_id')
        if service_id:
            pending_reviews = pending_reviews.filter(service_id=service_id)

        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            pending_reviews = pending_reviews.filter(created_at__date__gte=date_from)

        serializer = ReviewAdminSerializer(pending_reviews, many=True, context={'request': request})

        # Статистика
        total_pending = pending_reviews.count()

        return Response({
            "statistics": {
                "total_pending": total_pending,
                "pending_by_service": pending_reviews.values('service__name').annotate(count=Count('id'))
            },
            "reviews": serializer.data
        })


class AdminReviewDetailAPIView(APIView):
    """
    GET: Детали отзыва (админ)
    PUT: Полное обновление отзыва (админ)
    PATCH: Частичное обновление отзыва (админ)
    DELETE: Удалить отзыв (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReviewAdminSerializer

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None

    def get(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewAdminSerializer(review, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewAdminSerializer(review, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewAdminSerializer(review, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        review.delete()
        return Response(
            {"message": "Отзыв успешно удален"},
            status=status.HTTP_200_OK
        )


class AdminReviewPublishAPIView(APIView):
    """
    PATCH: Опубликовать/скрыть отзыв (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReviewPublishSerializer

    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что указан статус публикации
        is_published = request.data.get('is_published')
        if is_published is None:
            return Response(
                {"error": "Не указан статус публикации (is_published)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Меняем статус публикации
        review.is_published = is_published
        review.save()

        action = "опубликован" if is_published else "скрыт"
        serializer = ReviewAdminSerializer(review, context={'request': request})

        return Response({
            "message": f"Отзыв успешно {action}",
            "review": serializer.data
        })


class AdminUserListAPIView(APIView):
    """
    GET: Список всех пользователей (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')

        # Фильтрация по роли
        role = request.query_params.get('role')
        if role:
            users = users.filter(role=role)

        # Фильтрация по активности
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            users = users.filter(is_active=is_active.lower() == 'true')

        # Поиск по email, имени, фамилии
        search = request.query_params.get('search')
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )

        # Фильтрация по дате регистрации (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            users = users.filter(date_joined__date__gte=date_from)

        # Фильтрация по дате регистрации (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            users = users.filter(date_joined__date__lte=date_to)

        # Аннотация с количеством заявок и отзывов
        users = users.annotate(
            order_count=Count('orders', distinct=True),
            review_count=Count('reviews', distinct=True)
        )

        serializer = UserAdminListSerializer(users, many=True)
        return Response(serializer.data)


class AdminUserDetailAPIView(APIView):
    """
    GET: Детали пользователя (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем статистику пользователя
        user_data = UserAdminDetailSerializer(user).data

        # Дополнительная статистика
        orders = user.orders.all()
        reviews = user.reviews.all()

        # Статистика по заявкам
        order_stats = {
            "total": orders.count(),
            "by_status": orders.values('status').annotate(count=Count('id')),
            "recent_orders": orders.order_by('-created_at')[:5].values('id', 'service__name', 'status', 'created_at')
        }

        # Статистика по отзывам
        review_stats = {
            "total": reviews.count(),
            "published": reviews.filter(is_published=True).count(),
            "average_rating": reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] if reviews.exists() else None,
            "recent_reviews": reviews.order_by('-created_at')[:5].values('id', 'service__name', 'rating', 'created_at')
        }

        return Response({
            "user": user_data,
            "statistics": {
                "orders": order_stats,
                "reviews": review_stats
            }
        })


class AdminUserRoleUpdateAPIView(APIView):
    """
    PATCH: Изменить роль пользователя (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что пользователь не меняет свою собственную роль
        if user == request.user:
            return Response(
                {"error": "Вы не можете изменить свою собственную роль"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что указана новая роль
        serializer = UserRoleUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Сохраняем новую роль
        old_role = user.role
        serializer.save()

        return Response({
            "message": f"Роль пользователя успешно изменена с '{old_role}' на '{user.role}'",
            "user": UserAdminDetailSerializer(user).data
        })