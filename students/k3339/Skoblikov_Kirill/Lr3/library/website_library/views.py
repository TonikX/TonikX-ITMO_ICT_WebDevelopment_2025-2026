import calendar
from datetime import date, timedelta
from django.db.models import Count, ExpressionWrapper, F, FloatField
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, LibraryReader, Reading, BookSet, ReaderRegistration, Hall, LibraryEmployee
from .serializers import BookSerializer, LibraryReaderSerializer, EducationStatsSerializer, \
    MonthlyLibraryReportSerializer, HallSerializer, EmployeesUsernameSerializer, ReadingSerializer
from drf_yasg.utils import swagger_auto_schema


class AllBookView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список всех книг",
        tags=["Books"],
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({"Books": serializer.data})

    @swagger_auto_schema(
        operation_description="Создать новую книгу",
        tags=["Book"],
        request_body=BookSerializer,
        responses={
            201: BookSerializer,
            400: "Ошибка валидации"
        }
    )
    def post(self, request):
        book = request.data
        serializer = BookSerializer(data=book)
        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()

        return Response({"Success": "Book '{}' created succesfully.".format(book_saved.book_name)})


class ConcreteBookView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Изменение книги по ID",
        tags=["Book"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID книги",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Книга успешно изменена"),
            404: openapi.Response("Книга не найдена")
        }
    )
    def patch(self, request, pk):
        book = Book.objects.get(book_id=pk)
        if not book:
            return Response({"success": False, "error": f"Книга с ID {pk} не найдена"})

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": f"Книга с ID {pk} успешно изменена"})

        return Response({"success": False, "error": f"Книга с ID {pk} не изменена"})

    @swagger_auto_schema(
        operation_description="Получить информацию о книге",
        tags=["Book"],
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request, pk):
        book = Book.objects.get(book_id=pk)
        serializer = BookSerializer(book)
        return Response({"Books": serializer.data})

    @swagger_auto_schema(
        operation_description="Удаление книги по ID",
        tags=["Book"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID книги",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Книга успешно удалена"),
            404: openapi.Response("Книга не найдена")
        }
    )
    def delete(self, request, pk):
        book = Book.objects.get(book_id=pk)
        if not book:
            return Response({"success": False, "error": f"Книга с ID {pk} не найдена"})

        data = {'id': book.book_id, 'name': book.book_name}
        book.delete()
        return Response({"Succes": True, "message": f'Книга "{data["name"]}" (ID: {data["id"]}) успешно удалена'})


class LibraryReaderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список всех читателей",
        tags=["Readers"],
        responses={200: LibraryReaderSerializer(many=True)}
    )
    def get(self, request):
        readers = LibraryReader.objects.all()
        serializer = LibraryReaderSerializer(readers, many=True)
        return Response({"Readers": serializer.data})

    @swagger_auto_schema(
        operation_description="Создать нового читателя",
        tags=["Reader"],
        request_body=LibraryReaderSerializer,
        responses={201: LibraryReaderSerializer}
    )
    def post(self, request):
        reader = request.data
        serializer = LibraryReaderSerializer(data=reader)
        if serializer.is_valid(raise_exception=True):
            reader_saved = serializer.save()

        return Response({"Success": "Reader '{}' created succesfully.".format(reader_saved.reader_card_number)})


class ConcreteLibraryReaderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Изменение читателя по ID",
        tags=["Reader"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID читателя",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Читатель успешно изменен"),
            404: openapi.Response("Читатель не найден")
        }
    )
    def patch(self, request, pk):
        reader = LibraryReader.object.get(reader_id=pk)
        if not reader:
            return Response({"success": False, "error": f"Читатель с ID {pk} не найден"})

        serializer = LibraryReaderSerializer(reader, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": f"Читатель с ID {pk} успешно изменен"})

        return Response({"success": False, "error": f"Читатель с ID {pk} не изменен"})

    @swagger_auto_schema(
        operation_description="Удаление читателя по ID",
        tags=["Reader"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID читателя",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Читатель успешно удален"),
            404: openapi.Response("Читатель не найден")
        }
    )
    def delete(self, request, pk):
        reader = LibraryReader.objects.get(reader_id=pk)
        if not reader:
            return Response({"success": False, "error": f"Читатель с ID {pk} не найден"})

        data = {'id': reader.reader_id, 'name': reader.first_name, 'last_name': reader.last_name}
        reader.delete()
        return Response({"Succes": True, "message": f'Читатель "{data["name"]} {data["last_name"]}" (ID: {data["id"]}) успешно удален'})


class LibraryReaderDelete(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Удалить читателя по ID",
        tags=["Readers"],
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="ID читателя",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: "Читатель удален",
            404: "Читатель не найден"
        }
    )
    def delete(self, request, pk):
        reader = LibraryReader.objects.filter(id=pk).first()
        if not reader:
            return Response({"success": False, "error": f"Читатель с ID {pk} не найден"})

        data = {'id': reader.reader_id, 'name': reader.first_name, 'last_name': reader.last_name}
        reader.delete()
        return Response({"Succes": True,
                         "message": f'Читатель "{data["name"]} {data["last_name"]}" (ID: {data["id"]}) успешно удален'})


class LibraryReaderStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Статистика читателей по уровню образования",
        tags=["Statistics"],
        responses={200: EducationStatsSerializer(many=True)}
    )
    def get(self, request):
        readers_cnt = LibraryReader.objects.count()
        if readers_cnt == 0:
            return Response({"detail": "Нет данных о читателях"})

        education_stats = LibraryReader.objects.values('education').annotate(count=Count('education')) \
            .annotate(percentage=ExpressionWrapper(F('count') * 100.0 / readers_cnt,output_field=FloatField())) \
            .order_by('education')
        education_names = {'se': 'Среднее образование', 'he': 'Высшее образование', 'ad': 'Ученая степень'}
        result = []
        for stat in education_stats:
            result.append({
                'education_type': education_names.get(stat['education'], 'Не указано'),
                'education_code': stat['education'],
                'count': stat['count'],
                'percentage': round(stat['percentage'], 2)
            })

        result.append({
            'education_type': 'Всего читателей',
            'education_code': 'total',
            'count': readers_cnt,
            'percentage': 100.00
        })
        serializer = EducationStatsSerializer(result, many=True)

        return Response({"statistics": serializer.data})


class YoungLibraryReaderStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Количество читателей младше 20 лет",
        tags=["Statistics"],
        responses={
            200: openapi.Response("Количество читателей"),
            404: "Нет читателей младше 20 лет"
        }
    )
    def get(self, request):
        twenty_years_ago = date.today() - timedelta(days=365 * 20)
        youngs = LibraryReader.objects.filter(birth_date__gt=twenty_years_ago).count()
        if youngs == 0:
            return Response({"detail": "В библиотеке нет читателей моложе 20 лет"})

        return Response({"detail": f"В библиотеке {youngs} читателей моложе 20 лет"})


class ReaderReadingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Список книг у читателя",
        tags=["Reader"],
        manual_parameters=[
            openapi.Parameter(
                "reader_id",
                openapi.IN_PATH,
                description="ID читателя",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request, id):
        reader = LibraryReader.objects.get(reader_id=id)
        readings = Reading.objects.filter(reader=reader).select_related('book')
        book_ids = readings.values_list('book_id', flat=True)
        books = Book.objects.filter(book_id__in=book_ids)
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)


class BadReaderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Читатели, которые взяли книгу более месяца назад",
        tags=["Statistics"],
        responses={
            200: openapi.Response("Список читателей"),
            404: "Нет плохих читателей"
        }
    )
    def get(self, request):
        month_ago = date.today() - timedelta(days=30)
        reader_ids = Reading.objects.filter(issued_date__lt=month_ago, returned_date__isnull=True) \
                            .values_list('reader_id', flat=True).distinct()
        readers = LibraryReader.objects.filter(reader_id__in=reader_ids)
        serializer = LibraryReaderSerializer(readers, many=True)

        return Response(serializer.data)


class ReadingRareBook(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Читатели, которые взяли редкую книгу",
        tags=["Statistics"],
        responses={
            200: openapi.Response("Читатели"),
            404: "Нет подходящих читателей"
        }
    )
    def get(self, request):
        rare_books = Book.objects.values('book_name', 'authors').annotate(copies=Count('book_id')).filter(copies__lte=2)
        rare_book_ids = []
        for book in rare_books:
            ids = Book.objects.filter(
                book_name=book['book_name'],
                authors=book['authors']
            ).values_list('book_id', flat=True)
            rare_book_ids.extend(ids)

        readers = LibraryReader.objects.filter(
            reading__book_id__in=rare_book_ids,
            reading__returned_date__isnull=True
        ).distinct()

        serializer = LibraryReaderSerializer(readers, many=True)
        return Response(serializer.data)


class MonthlyLibraryReportView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Ежемесячный отчет библиотеки",
        tags=["Reports"],
        manual_parameters=[
            openapi.Parameter(
                "year",
                openapi.IN_PATH,
                description="Год отчета",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                "month",
                openapi.IN_PATH,
                description="Месяц отчета (1-12)",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: MonthlyLibraryReportSerializer}
    )
    def get(self, request, year, month):
        days_in_month = calendar.monthrange(year, month)[1]
        dates = [date(year, month, day) for day in range(1, days_in_month + 1)]
        daily_statistics = []

        def transform_hall_stats(stats_qs):
            # stats_qs — QuerySet с values('hall__hall_number', 'hall__hall_name') и annotate(count=...)
            return [
                {
                    'hall_number': item['hall__hall_number'],
                    'hall_name': item['hall__hall_name'],
                    'count': item['count']
                }
                for item in stats_qs
            ]

        books_per_hall_qs = BookSet.objects.values("hall__hall_number", "hall__hall_name") \
            .annotate(count=Count("book"))
        books_per_hall = transform_hall_stats(books_per_hall_qs)
        total_books = BookSet.objects.count()

        readers_per_hall_qs = LibraryReader.objects.values("hall__hall_number", "hall__hall_name") \
            .annotate(count=Count("reader_id"))
        readers_per_hall = transform_hall_stats(readers_per_hall_qs)
        total_readers = LibraryReader.objects.count()
        for current_date in dates:
            daily_statistics.append({
                "date": current_date,
                "books": {
                    "per_hall": books_per_hall,
                    "total": total_books
                },
                "readers": {
                    "per_hall": readers_per_hall,
                    "total": total_readers
                }
            })

        month_registrations = ReaderRegistration.objects.filter(
            registration_date__year=year,
            registration_date__month=month
        )

        registrations_per_hall_qs = month_registrations.values("hall__hall_number", "hall__hall_name") \
            .annotate(count=Count("reader", distinct=True))
        registrations_per_hall = transform_hall_stats(registrations_per_hall_qs)

        total_registrations = month_registrations.values("reader").distinct().count()
        report = {
            "period": f"{month:02}.{year}",
            "daily_statistics": daily_statistics,
            "registrations": {
                "per_hall": registrations_per_hall,
                "total": total_registrations
            }
        }

        serializer = MonthlyLibraryReportSerializer(report)
        return Response(serializer.data)


class HallView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список всех заллов",
        tags=["Halls"],
        responses={200: HallSerializer(many=True)}
    )
    def get(self, request):
        halls = Hall.objects.all()
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Создать новый зал",
        tags=["Hall"],
        request_body=HallSerializer,
        responses={
            201: HallSerializer,
            400: "Ошибка валидации"
        }
    )
    def post(self, request):
        hall = request.data
        serializer = HallSerializer(data=hall)
        if serializer.is_valid(raise_exception=True):
            hall_saved = serializer.save()

        return Response({"Success": "Hall '{}' created succesfully.".format(hall_saved.hall_name)})


class ConcreteHallView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить информацию о зале",
        tags=["Hall"],
        responses={200: HallSerializer(many=True)}
    )
    def get(self, request, pk):
        hall = Hall.objects.get(hall_number=pk)
        serializer = HallSerializer(hall)
        return Response({"Hall": serializer.data})

    @swagger_auto_schema(
        operation_description="Удаление зала по ID",
        tags=["Hall"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID зала",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Зал успешно удален"),
            404: openapi.Response("Зал не найден")
        }
    )
    def delete(self, request, pk):
        hall = Hall.objects.get(hall_number=pk)
        if not hall:
            return Response({"success": False, "error": f"Зал с ID {pk} не найден"})

        data = {'name': hall.hall_name}
        hall.delete()
        return Response({"Succes": True, "message": f'"{data["name"]}" успешно удален'})

    @swagger_auto_schema(
        operation_description="Изменение зала по ID",
        tags=["Hall"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID зала",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Зал успешно изменен"),
            404: openapi.Response("Зал не найден")
        }
    )
    def patch(self, request, pk):
        hall = Hall.objects.get(hall_number=pk)
        if not hall:
            return Response({"success": False, "error": f"Зал с ID {pk} не найден"})

        serializer = HallSerializer(hall, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": f"Зал с ID {pk} успешно изменен"})

        return Response({"success": False, "error": f"Зал с ID {pk} не изменен"})


class LibraryEmployeeUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список всех юзернеймов сотрудников",
        tags=["Employees"],
        responses={200: EmployeesUsernameSerializer(many=True)}
    )
    def get(self, request):
        usernames = LibraryEmployee.objects.values_list('username', flat=True)
        serializer = EmployeesUsernameSerializer(usernames, many=True)
        username_list = [item['username'] for item in serializer.data]
        return Response({'usernames': username_list})


class ReadingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список всех чтений",
        tags=["Readings"],
        responses={200: ReadingSerializer(many=True)}
    )
    def get(self, request):
        readings = Reading.objects.all()
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Выдать книгу на дом",
        tags=["Reading"],
        request_body=ReadingSerializer,
        responses={
            201: ReadingSerializer,
            400: "Ошибка валидации"
        }
    )
    def post(self, request):
        reading = request.data
        serializer = ReadingSerializer(data=reading)
        if serializer.is_valid(raise_exception=True):
            reading_saved = serializer.save()

        return Response({"Success": "Reading '{}' created succesfully.".format(reading_saved.reading_id)})


class ConcreteReadingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить информацию о чтении",
        tags=["Reading"],
        responses={200: ReadingSerializer(many=True)}
    )
    def get(self, request, pk):
        reading = Reading.objects.get(reading_id=pk)
        serializer = ReadingSerializer(reading)
        return Response({"Reading": serializer.data})

    @swagger_auto_schema(
        operation_description="Удаление чтения по ID",
        tags=["Reading"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID чтения",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Чтение успешно удалено"),
            404: openapi.Response("Чтение не найдено")
        }
    )
    def delete(self, request, pk):
        reading = Reading.objects.get(reading_id=pk)
        if not reading:
            return Response({"success": False, "error": f"Чтение с ID {pk} не найдено"})

        data = {'id': reading.reading_id}
        reading.delete()
        return Response({"Succes": True, "message": f'Чтение с ID: "{data["id"]}" успешно удалено'})

    @swagger_auto_schema(
        operation_description="Изменение чтения по ID",
        tags=["Reading"],
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="ID чтения",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Чтение успешно изменено"),
            404: openapi.Response("Чтение не найдено")
        }
    )
    def patch(self, request, pk):
        reading = Reading.objects.get(reading_id=pk)
        if not reading:
            return Response({"success": False, "error": f"Чтение с ID {pk} не найдено"})

        serializer = ReadingSerializer(reading, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": f"Чтение с ID {pk} успешно изменено"})

        return Response({"success": False, "error": f"Чтение с ID {pk} не изменено"})