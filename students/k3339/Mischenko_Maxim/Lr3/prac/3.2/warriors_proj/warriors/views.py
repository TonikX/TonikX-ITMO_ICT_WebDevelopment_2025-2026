from rest_framework import generics
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from .models import Warrior, Skill, Profession
from .serializers import WarriorSerializer, \
    SkillSerializer, SkillCreateSerializer, WarriorSkillSerializer, WarriorProfessionSerializer, \
    WarriorProfessionSkillsSerializer, ProfessionCreateSerializer, WarriorCreateUpdateSerializer

class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})

class SkillsApiView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    def post(self, request):
        skills = request.data.get('skill')
        serializer = SkillCreateSerializer(data=skills)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
            return Response({"Success": "Skill '{}' created successfully.".format(skill_saved.title)})
        return Response({"Error": "Skill not created."})

class WarriorsSkillsView(generics.ListAPIView):
    serializer_class = WarriorSkillSerializer
    queryset = Warrior.objects.all()

class WarriorProfessionsView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.all()

class WarriorProfSkillAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                warrior = Warrior.objects.get(pk=pk)
                serializer = WarriorProfessionSkillsSerializer(warrior)
                return Response({"Warrior": serializer.data})
            except Warrior.DoesNotExist:
                return Response({"Error": "Warrior not found."})
        else:
            queryset = Warrior.objects.all()
            serializer = WarriorProfessionSkillsSerializer(queryset, many=True)
            return Response({"Warriors": serializer.data})

class DeleteWarriorView(DestroyAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()

class UpdateWarriorView(UpdateAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()

class ProfessionCreateView(APIView):

   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionCreateSerializer(data=profession)

       if serializer.is_valid(raise_exception=True):
           profession_saved = serializer.save()

       return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})

class WarriorListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

class WarriorCreateAPIView(generics.CreateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

class WarriorWithProfessionListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.select_related('profession').all()
    serializer_class = WarriorSerializer

class WarriorWithSkillsListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.prefetch_related('skill').all()
    serializer_class = WarriorSerializer

class WarriorDetailAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.select_related('profession').prefetch_related('skill').all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'

class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'

class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorCreateUpdateSerializer
    lookup_field = 'id'
