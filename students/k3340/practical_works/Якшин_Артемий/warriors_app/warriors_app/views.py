from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import (
    WarriorSerializer,
    ProfessionSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    SkillCreateSerializer,
    WarriorWithProfessionSerializer,
    WarriorWithSkillsSerializer,
    WarriorDetailSerializer
)


class WarriorAPIView(APIView):
    """
    Представление для получения списка всех воинов
    """
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):
    """
    Представление для создания профессии
    """
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionCreateSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created successfully.".format(profession_saved.title)})


class ProfessionAPIView(APIView):
    """
    Представление для получения списка всех профессий
    """
    def get(self, request):
        professions = Profession.objects.all()
        serializer = ProfessionSerializer(professions, many=True)
        return Response({"Professions": serializer.data})


class SkillAPIView(APIView):
    """
    Представление для получения списка всех умений и создания нового
    """
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({
            "Success": "Skill '{}' created successfully.".format(skill_saved.title)
        })


class WarriorWithProfessionsView(APIView):
    """
    Представление для получения всех воинов с их профессиями
    """
    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorWithProfessionSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorWithSkillsView(APIView):
    """
    Представление для получения всех воинов с их скилами
    """
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorWithSkillsSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorDetailView(APIView):
    """
    Представление для работы с конкретным воином (получение, удаление, редактирование)
    """
    def get(self, request, warrior_id):
        """
        Получение полной информации о воине (профессия + скилы)
        """
        warrior = get_object_or_404(Warrior, id=warrior_id)
        serializer = WarriorDetailSerializer(warrior)
        return Response({"Warrior": serializer.data})

    def delete(self, request, warrior_id):
        """
        Удаление воина по id
        """
        warrior = get_object_or_404(Warrior, id=warrior_id)
        warrior_name = warrior.name
        warrior.delete()
        return Response({
            "Success": "Warrior '{}' deleted successfully.".format(warrior_name)
        }, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, warrior_id):
        """
        Полное обновление информации о воине
        """
        warrior = get_object_or_404(Warrior, id=warrior_id)
        serializer = WarriorSerializer(warrior, data=request.data)

        if serializer.is_valid(raise_exception=True):
            warrior_updated = serializer.save()

        return Response({
            "Success": "Warrior '{}' updated successfully.".format(warrior_updated.name)
        })

    def patch(self, request, warrior_id):
        """
        Частичное обновление информации о воине
        """
        warrior = get_object_or_404(Warrior, id=warrior_id)
        serializer = WarriorSerializer(warrior, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            warrior_updated = serializer.save()

        return Response({
            "Success": "Warrior '{}' updated successfully.".format(warrior_updated.name)
        })
