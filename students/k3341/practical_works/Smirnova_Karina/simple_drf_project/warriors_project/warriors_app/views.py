from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Warrior, Skill
from .serializers import WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, WarriorFullSerializer, \
    WarriorProfessionSerializer, WarriorSkillSerializer


class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})

class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionCreateSerializer(data=profession)
        if serializer.is_valid(raise_exception=True):profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})

class SkillListView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({'skills': serializer.data})

class SkillCreateView(APIView):
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            skill = serializer.save()
            return Response({'success': f"Skill '{skill.title}' created successfully."})
        return Response(serializer.errors, status=400)

class WarriorWithProfessionListAPIView(generics.ListAPIView):
    """
    Воины + профессия
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorProfessionSerializer

class WarriorWithSkillsListAPIView(generics.ListAPIView):
    """
    Воины + скилы
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorSkillSerializer

class WarriorDetailAPIView(generics.RetrieveAPIView):
    """
    Один воин по id + профессия + скиллы
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer

class WarriorDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление воина
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer

class WarriorUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование информации о воине
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer
