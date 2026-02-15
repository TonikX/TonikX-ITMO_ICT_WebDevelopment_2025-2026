from django.urls import path
from .views import *
from . import views_analytics as av

urlpatterns = [
    # halls
    path("halls/", HallListCreateAPIView.as_view()),
    path("halls/<int:pk>/", HallRetrieveUpdateDestroyAPIView.as_view()),

    # authors
    path("authors/", AuthorListCreateAPIView.as_view()),
    path("authors/<int:pk>/", AuthorRetrieveUpdateDestroyAPIView.as_view()),

    # books
    path("books/", BookListCreateAPIView.as_view()),
    path("books/<int:pk>/", BookRetrieveUpdateDestroyAPIView.as_view()),

    # readers
    path("readers/", ReaderListCreateAPIView.as_view()),
    path("readers/<int:pk>/", ReaderRetrieveUpdateDestroyAPIView.as_view()),
    path("readers/purge-old/", PurgeOldReadersAPIView.as_view(), name="readers-purge-old"),

    # loans
    path("loans/", LoanListCreateAPIView.as_view()),
    path("loans/<int:pk>/", LoanRetrieveUpdateDestroyAPIView.as_view()),

    path("stock/", BookStockListCreateAPIView.as_view(), name="stock-list-create"),
    path("stock/<int:pk>/", BookStockRetrieveUpdateDestroyAPIView.as_view(), name="stock-detail"),

    path("movements/", BookMovementListCreateAPIView.as_view(), name="movement-list-create"),
    path("movements/<int:pk>/", BookMovementRetrieveUpdateDestroyAPIView.as_view(), name="movement-detail"),

    path("analytics/readers/<int:reader_id>/books/", av.ReaderBooksAPIView.as_view()),
    path("analytics/loans/overdue/", av.OverdueLoansAPIView.as_view()),
    path("analytics/loans/rare/", av.RareBooksLoansAPIView.as_view()),
    path("analytics/readers/under20/", av.ReadersUnder20APIView.as_view()),
    path("analytics/readers/education-stats/", av.ReaderEducationStatsAPIView.as_view()),
    path("analytics/monthly-report/", MonthlyReportAPIView.as_view(), name="monthly-report"),


    path("book-codes/", BookCodeHistoryListCreateAPIView.as_view()),
    path("book-codes/<int:pk>/", BookCodeHistoryRetrieveUpdateDestroyAPIView.as_view()),

    path("reader-hall-history/", ReaderHallHistoryListCreateAPIView.as_view()),
    path("reader-hall-history/<int:pk>/", ReaderHallHistoryRetrieveUpdateDestroyAPIView.as_view()),

    path("membership-events/", ReaderMembershipHistoryListCreateAPIView.as_view()),
    path("membership-events/<int:pk>/", ReaderMembershipHistoryRetrieveUpdateDestroyAPIView.as_view()),

    path("ticket-history/", ReaderTicketHistoryListCreateAPIView.as_view()),
    path("ticket-history/<int:pk>/", ReaderTicketHistoryRetrieveUpdateDestroyAPIView.as_view()),
]
