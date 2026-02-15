from .models import Warrior
from rest_framework import generics
from .models import Warrior
from .serializers import (
    WarriorWithProfessionSerializer,
    WarriorWithSkillsSerializer,
    WarriorFullSerializer,
    WarriorUpdateSerializer
)

class WarriorWithProfessionListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorWithProfessionSerializer

class WarriorWithSkillsListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorWithSkillsSerializer


class WarriorDetailAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer
    lookup_field = "id"

class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    lookup_field = "id"


class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorUpdateSerializer
    lookup_field = "id"
