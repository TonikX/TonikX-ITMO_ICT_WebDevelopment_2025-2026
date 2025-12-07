from rest_framework import generics
from .models import Client, Deposit, Credit
from .serializers import ClientSerializer, DepositSerializer, CreditSerializer

class ClientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    lookup_field = 'pk'
    serializer_class = ClientSerializer

class DepositListCreateAPIView(generics.ListCreateAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

class DepositRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deposit.objects.all()
    lookup_field = 'pk'
    serializer_class = DepositSerializer

class CreditListCreateAPIView(generics.ListCreateAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

class CreditRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Credit.objects.all()
    lookup_field = 'pk'
    serializer_class = CreditSerializer