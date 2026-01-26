from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import (
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    WarriorFullSerializer,
    WarriorUpdateSerializer,
    WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, SkillCreateSerializer
)

# 1. Вывод полной информации о всех войнах и их профессиях
class WarriorProfessionListAPIView(generics.ListAPIView):
    """
    Эндпоинт для вывода всех воинов с их профессиями
    GET /war/warriors/professions/
    """
    queryset = Warrior.objects.all().select_related('profession')
    serializer_class = WarriorProfessionSerializer


# 2. Вывод полной информации о всех войнах и их скилах
class WarriorSkillListAPIView(generics.ListAPIView):
    """
    Эндпоинт для вывода всех воинов с их скилами
    GET /war/warriors/skills/
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorSkillSerializer


# 3. Вывод полной информации о войне (по id), его профессии и скилах
class WarriorRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт для вывода полной информации о воине по ID
    GET /war/warriors/<id>/
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer
    lookup_field = 'id'


# 4. Удаление война по id
class WarriorDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления воина по ID
    DELETE /war/warriors/delete/<id>/
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'


# 5. Редактирование информации о войне
class WarriorUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для редактирования информации о воине
    PUT /war/warriors/update/<id>/
    PATCH /war/warriors/update/<id>/
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorUpdateSerializer
    lookup_field = 'id'


# Дополнительно: Список всех воинов (базовый)
class WarriorListAPIView(generics.ListAPIView):
    """
    Эндпоинт для вывода списка всех воинов
    GET /war/warriors/
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


# Дополнительно: Создание нового воина
class WarriorCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания нового воина
    POST /war/warriors/create/
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer



class ProfessionCreateView(APIView):
    def post(self, request):
        if 'profession' in request.data:
            profession = request.data.get("profession")
        else:
            profession = request.data

        serializer = ProfessionCreateSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created successfully.".format(profession_saved.title)})


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):
    def post(self, request):
        if 'skill' in request.data:
            skill_data = request.data.get("skill")
        else:
            skill_data = request.data

        serializer = SkillCreateSerializer(data=skill_data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": "Skill '{}' created successfully.".format(skill_saved.title)})

