from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import (
    WarriorSerializer, WarriorNestedSerializer, WarriorCreateSerializer,
    SkillSerializer, ProfessionSerializer, SkillOfWarriorSerializer
)


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    def post(self, request):
        skill_data = request.data.get("skill")
        serializer = SkillSerializer(data=skill_data)
        
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        
        return Response({"Success": "Skill '{}' created successfully.".format(skill_saved.title)})


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created successfully.".format(profession_saved.title)})


# Generic API Views
class WarriorListAPIView(generics.ListAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorCreateAPIView(generics.CreateAPIView):
    serializer_class = WarriorCreateSerializer
    queryset = Warrior.objects.all()


class ProfessionCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfessionSerializer
    queryset = Profession.objects.all()


# Полная информация о воинах с профессиями
class WarriorWithProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorNestedSerializer
    queryset = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()


# Полная информация о воинах со скиллами
class WarriorWithSkillsListAPIView(generics.ListAPIView):
    serializer_class = WarriorNestedSerializer
    queryset = Warrior.objects.prefetch_related('skillofwarrior_set__skill').all()


# Полная информация о конкретном воине
class WarriorDetailAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorNestedSerializer
    queryset = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()


# Удаление воина
class WarriorDestroyAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()


# Редактирование воина
class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorCreateSerializer
    queryset = Warrior.objects.all()


# Полный CRUD для воина
class WarriorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WarriorNestedSerializer
    queryset = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()
