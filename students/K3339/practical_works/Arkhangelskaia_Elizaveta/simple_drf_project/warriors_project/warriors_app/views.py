from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Warrior, Skill
from .serializers import *


class WarriorAPIView(generics.ListAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()

class ProfessionCreateView(generics.CreateAPIView):
   serializer_class = ProfessionCreateSerializer
   queryset = Profession.objects.all()

class SkillAPIView(generics.ListAPIView):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class SkillsCreateView(generics.CreateAPIView):
    serializer_class = SkillCreateSerializer
    queryset = Skill.objects.all()


class WarriorProfessionAPIView(generics.ListAPIView):
    queryset = Warrior.objects.select_related('profession').all()
    serializer_class = WarriorSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        allowed = ['id', 'name', 'race', 'level', 'profession']
        serializer.child.fields = {field: serializer.child.fields[field] for field in allowed}
        return serializer

class WarriorSkillsAPIView(generics.ListAPIView):
    queryset = Warrior.objects.prefetch_related('skillofwarrior_set__skill').all()
    serializer_class = WarriorSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        allowed = ['id', 'name', 'race', 'level', 'skill']
        serializer.child.fields = {field: serializer.child.fields[field] for field in allowed}
        return serializer

class WarriorDetailAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'id'

class WarriorDestroyAPIView(generics.DestroyAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'id'


class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorUpdateSerializer
    lookup_field = 'id'