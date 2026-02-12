from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import Warrior, Skill
from .serializers import WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, SkillCreateSerializer, WarriorFullSerializer, WarriorCreateSerializer


class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})


class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()


class WarriorSkillListAPIView(generics.ListAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()


class WarriorRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()


class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()


class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.all()


class ProfessionCreateView(APIView):

   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionCreateSerializer(data=profession)

       if serializer.is_valid(raise_exception=True):
           profession_saved = serializer.save()

       return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class SkillListAPIView(APIView):
    """Получить список всех скиллов"""

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"skills": serializer.data})


class SkillCreateAPIView(APIView):
    """Создать новый скилл"""

    def post(self, request):
        skill_data = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill_data)

        if serializer.is_valid(raise_exception=True):
            created_skill = serializer.save()

        return Response({"Success": f"Skill '{created_skill.title}' created successfully."})


class WarriorCreateAPIView(generics.CreateAPIView):
   serializer_class = WarriorCreateSerializer
   queryset = Warrior.objects.all()

   def perform_create(self, serializer):
       serializer.save(owner=self.request.user)