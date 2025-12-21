from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import (
    WarriorSerializer,
    WarriorUpdateSerializer,
    WarriorCreateSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    SkillCreateSerializer,
    WarriorExtendedSerializer,
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    SkillOfWarriorCreateSerializer,
)

class WarriorListAPIView(generics.ListAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()

class ProfessionCreateAPIView(generics.CreateAPIView):
   serializer_class = ProfessionCreateSerializer
   queryset = Profession.objects.all()

class SkillListAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

class SkillCreateAPIView(APIView):
    def post(self, request):
        skill_data = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill_data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": f"Skill '{skill_saved.title}' created succesfully."})

class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.all()

class WarriorSkillListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillSerializer
    queryset = Warrior.objects.all()

class WarriorRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = WarriorExtendedSerializer
    queryset = Warrior.objects.all()

class WarriorRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WarriorUpdateSerializer
    queryset = Warrior.objects.all()

class WarriorCreateAPIView(generics.CreateAPIView):
   serializer_class = WarriorCreateSerializer
   queryset = Warrior.objects.all()

   def perform_create(self, serializer):
       serializer.save() 

class SkillOfWarriorCreateAPIView(generics.CreateAPIView):
   serializer_class = SkillOfWarriorCreateSerializer
   queryset = SkillOfWarrior.objects.all()

   def perform_create(self, serializer):
       serializer.save() 