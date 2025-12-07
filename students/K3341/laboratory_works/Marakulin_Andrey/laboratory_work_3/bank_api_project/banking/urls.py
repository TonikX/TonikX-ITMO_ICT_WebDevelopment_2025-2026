from django.urls import path
from .views import (
    ClientListCreateAPIView, ClientRetrieveUpdateDestroyAPIView,
    DepositListCreateAPIView, DepositRetrieveUpdateDestroyAPIView,
    CreditListCreateAPIView, CreditRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('clients/', ClientListCreateAPIView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-detail'),

    path('deposits/', DepositListCreateAPIView.as_view(), name='deposit-list-create'),
    path('deposits/<int:pk>/', DepositRetrieveUpdateDestroyAPIView.as_view(), name='deposit-detail'),

    path('credits/', CreditListCreateAPIView.as_view(), name='credit-list-create'),
    path('credits/<int:pk>/', CreditRetrieveUpdateDestroyAPIView.as_view(), name='credit-detail'),
]