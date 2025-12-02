from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import Warrior, Skill, SkillOfWarrior
from .serializers import (
    WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, SkillOfWarriorSerializer,
    WarriorProfessionSerializer, WarriorSkillSerializer, WarriorFullSerializer
)


class WarriorAPIView(APIView):

    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({'Warriors': serializer.data})

    def post(self, request):
        serializer = WarriorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessionCreateView(APIView):

    def post(self, request):
        profession = request.data.get('profession')
        serializer = ProfessionCreateSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Профессия '{}' успешно создана.".format(profession_saved.title)})


class SkillAPIView(APIView):

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({'Skills': serializer.data})

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarriorProfessionAPIView(APIView):
    '''
    Вывод полной информации о всех войнах и их профессиях
    '''

    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorProfessionSerializer(warriors, many=True)
        return Response({'Warriors': serializer.data})


class WarriorSkillAPIView(APIView):
    '''
    Вывод полной информации о всех войнах и их скилах
    '''

    def get(self, request):
        warriors = Warrior.objects.prefetch_related('warrior_skills__skill').all()
        serializer = WarriorSkillSerializer(warriors, many=True)
        return Response({'Warriors': serializer.data})


class WarriorDetailAPIView(APIView):
    '''
    Вывод полной информации о войне (по id), его профессиях и скилах
    Удаление война по id
    Редактирование информации о войне
    '''

    def get(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorFullSerializer(warrior)
        return Response({'Warrior': serializer.data})

    def post(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorSerializer(warrior, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorSerializer(warrior, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        warrior.delete()
        return Response({"Success": f"Воин '{warrior.name}' успешно удален."}, status=status.HTTP_204_NO_CONTENT)
