from django.urls import path
from .views import *

app_name = "library_app"

urlpatterns = [
    # ========================================================================
    # GET запросы (информация) - ПУНКТЫ 1-5 ИЗ ТЗ
    # ========================================================================

    # 1. Какие книги закреплены за заданным читателем?
    path('reader/<int:pk>/books/', ReaderBooksAPIView.as_view()),

    # 2. Кто из читателей взял книгу более месяца тому назад?
    path('loans/overdue/', OverdueLoansAPIView.as_view()),

    # 3. За кем из читателей закреплены редкие книги (≤2 экз.)?
    path('readers/rare-books/', RareBooksReadersAPIView.as_view()),

    # 4. Сколько в библиотеке читателей младше 20 лет?
    path('readers/young/', YoungReadersAPIView.as_view()),

    # 5. Процент читателей по образованию
    path('stats/education/', EducationStatsAPIView.as_view()),

    # Отчет за месяц (из ТЗ)
    path('reports/monthly/', MonthlyReportAPIView.as_view()),

    # Списки для просмотра
    path('books/', BookListAPIView.as_view()),
    path('readers/', ReaderListAPIView.as_view()),
    path('copies/', CopyOfBookListAPIView.as_view()),

    # ========================================================================
    # POST запросы (операции) - ПУНКТЫ 6-9 ИЗ ТЗ
    # ========================================================================

    # 6. Зарегистрировать нового читателя
    path('reader/register/', RegisterReaderAPIView.as_view()),

    # 7. Исключить неактивных читателей
    path('readers/remove-inactive/', RemoveInactiveReadersAPIView.as_view()),

    # 8. Списать книгу
    path('books/decommission/', DecommissionBookAPIView.as_view()),

    # 9. Добавить книгу в фонд
    path('books/add/', AddBookAPIView.as_view()),


    # Перемещение книги между залами (из ТЗ: "Книги могут перерегистрироваться в другом зале")
    path('copies/transfer-hall/', TransferCopyToHallAPIView.as_view()),

    # Изменение шифра книги (из ТЗ: "Шифр книги может измениться в результате переклассификации")
    path('books/<int:pk>/update-code/', UpdateBookCodeAPIView.as_view()),
]