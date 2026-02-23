from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

#____________________________________________________________________________
class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})

#____________________________________________________________________________
class ProfessionCreateView(APIView):

   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionCreateSerializer(data=profession)

       if serializer.is_valid(raise_exception=True):
           profession_saved = serializer.save()

       return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


#____________________________________________________________________________

class SkillAPIView(APIView):
   def get(self, request):
       skills = Skill.objects.all()
       serializer = SkillSerializer(skills, many=True)
       return Response({"Skills": serializer.data})

class SkillCreateView(APIView):
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"Success": "Скилл успешно добавлен."})

#____________________________________________________________________________

class WarriorFullInfo(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer

class WarriorFullWithSkill(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSkillsSerializer

class WarriorAllView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorAllSerializer

class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

