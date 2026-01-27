from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Skill, Warrior
from .serializers import *

class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"skills": serializer.data})
    
    def post(self, request):
       skill = request.data.get("skill")
       serializer = SkillSerializer(data=skill)

       if serializer.is_valid(raise_exception=True):
           skill_saved = serializer.save()

       return Response({"Success": "Skill '{}' created succesfully.".format(skill_saved.title)})

class WarriorWithProffesionAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorsWithProfessionSerializer

class WarriorWithSkillsAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorsWithSkillsSerializer

class WarriorFullByIdAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer

class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorUpdateSerializer

class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()

class WarriorCreateAPIView(generics.CreateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorCreateSerializer

class ProfessionCreateAPIView(generics.CreateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer