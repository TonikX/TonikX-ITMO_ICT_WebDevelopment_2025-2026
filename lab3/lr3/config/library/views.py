from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from datetime import timedelta, date
from django.utils import timezone

from .models import Hall, Book, Reader, BookIssue, BookInHall
from .serializers import HallSerializer, BookSerializer, ReaderSerializer, BookIssueSerializer, BookInHallSerializer


@method_decorator(swagger_auto_schema(tags=['Halls']), name='list')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='create')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='retrieve')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='update')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='partial_update')
@method_decorator(swagger_auto_schema(tags=['Halls']), name='destroy')
class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


@method_decorator(swagger_auto_schema(tags=['Books']), name='list')
@method_decorator(swagger_auto_schema(tags=['Books']), name='create')
@method_decorator(swagger_auto_schema(tags=['Books']), name='retrieve')
@method_decorator(swagger_auto_schema(tags=['Books']), name='update')
@method_decorator(swagger_auto_schema(tags=['Books']), name='partial_update')
@method_decorator(swagger_auto_schema(tags=['Books']), name='destroy')
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @swagger_auto_schema(tags=['Books'])
    @action(detail=False, methods=['get'])
    def rare(self, request):
        books = Book.objects.filter(bookinhall__copies__lte=2).distinct()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@method_decorator(swagger_auto_schema(tags=['Books in Halls']), name='list')
@method_decorator(swagger_auto_schema(tags=['Books in Halls']), name='create')
@method_decorator(swagger_auto_schema(tags=['Books in Halls']), name='retrieve')
@method_decorator(swagger_auto_schema(tags=['Books in Halls']), name='update')
@method_decorator(swagger_auto_schema(tags=['Books in Halls']), name='partial_update')
@method_decorator(swagger_auto_schema(tags=['Books in Halls']), name='destroy')
class BookInHallViewSet(viewsets.ModelViewSet):
    queryset = BookInHall.objects.all()
    serializer_class = BookInHallSerializer


@method_decorator(swagger_auto_schema(tags=['Readers']), name='list')
@method_decorator(swagger_auto_schema(tags=['Readers']), name='create')
@method_decorator(swagger_auto_schema(tags=['Readers']), name='retrieve')
@method_decorator(swagger_auto_schema(tags=['Readers']), name='update')
@method_decorator(swagger_auto_schema(tags=['Readers']), name='partial_update')
@method_decorator(swagger_auto_schema(tags=['Readers']), name='destroy')
class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=False, methods=['get'])
    def rare_books(self, request):
        issues = BookIssue.objects.filter(book__bookinhall__copies__lte=2)

        result = []
        for issue in issues:
            result.append(
                {
                    "reader": issue.reader.full_name,
                    "book": issue.book.title,
                }
            )

        unique = {
            (item["reader"], item["book"]): item
            for item in result
        }.values()

        return Response(list(unique))

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        reader = self.get_object()
        issues = BookIssue.objects.filter(reader=reader)

        books = [issue.book.title for issue in issues]

        return Response(books)

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=False, methods=['get'])
    def under_20(self, request):
        today = date.today()
        readers = Reader.objects.all()

        count = 0

        for r in readers:
            age = today.year - r.birth_date.year
            if age < 20:
                count += 1

        return Response({"readers_under_20": count})

    @swagger_auto_schema(tags=['Readers'])
    @action(detail=False, methods=['get'])
    def education_stats(self, request):

        total = Reader.objects.count()

        if total == 0:
            return Response({})

        primary = Reader.objects.filter(education="primary").count()
        secondary = Reader.objects.filter(education="secondary").count()
        higher = Reader.objects.filter(education="higher").count()
        degree = Reader.objects.filter(academic_degree=True).count()

        data = {
            "primary_%": round(primary / total * 100, 2),
            "secondary_%": round(secondary / total * 100, 2),
            "higher_%": round(higher / total * 100, 2),
            "degree_%": round(degree / total * 100, 2),
        }

        return Response(data)


@method_decorator(swagger_auto_schema(tags=['Issues']), name='list')
@method_decorator(swagger_auto_schema(tags=['Issues']), name='create')
@method_decorator(swagger_auto_schema(tags=['Issues']), name='retrieve')
@method_decorator(swagger_auto_schema(tags=['Issues']), name='update')
@method_decorator(swagger_auto_schema(tags=['Issues']), name='partial_update')
@method_decorator(swagger_auto_schema(tags=['Issues']), name='destroy')
class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.book_in_hall and instance.book_in_hall.copies > 0:
            instance.book_in_hall.copies -= 1
            instance.book_in_hall.save(update_fields=['copies'])

    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_return = old_instance.return_date
        instance = serializer.save()
        if instance.book_in_hall and instance.return_date and not old_return:
            instance.book_in_hall.copies += 1
            instance.book_in_hall.save(update_fields=['copies'])

    @swagger_auto_schema(tags=['Issues'])
    @action(detail=False, methods=['get'])
    def overdue(self, request):

        month_ago = timezone.now() - timedelta(days=30)

        issues = BookIssue.objects.filter(issue_date__lt=month_ago)

        readers = [issue.reader.full_name for issue in issues]

        return Response(list(set(readers)))