from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Warrior, Profession, Skill
from .serializers import (
    WarriorSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    SkillCreateSerializer,
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    WarriorDetailSerializer,
)


class WarriorAPIView(APIView):
    """
    Представление для просмотра всех воинов
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


class SkillAPIView(APIView):
    """
    Представление для просмотра всех скилов
    """

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):
    """
    Представление для создания скила
    """

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": "Skill '{}' created successfully.".format(skill_saved.title)})


class WarriorProfessionAPIView(APIView):
    """
    Вывод полной информации о всех воинах и их профессиях
    """

    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorProfessionSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorSkillAPIView(APIView):
    """
    Вывод полной информации о всех воинах и их скилах
    """

    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorSkillSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorDetailAPIView(APIView):
    """
    Вывод полной информации о воине по id (профессия и скилы)
    Удаление воина по id
    Редактирование информации о воине
    """

    def get(self, request, pk):
        warrior = get_object_or_404(
            Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill'),
            pk=pk
        )
        serializer = WarriorDetailSerializer(warrior)
        return Response(serializer.data)

    def put(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorSerializer(warrior, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": "Warrior '{}' updated successfully.".format(warrior.name), "Warrior": serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorSerializer(warrior, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": "Warrior '{}' updated successfully.".format(warrior.name), "Warrior": serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        warrior_name = warrior.name
        warrior.delete()
        return Response({"Success": "Warrior '{}' deleted successfully.".format(warrior_name)}, status=status.HTTP_204_NO_CONTENT)
