from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Warrior, Skill
from .serializers import (
    WarriorSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    WarriorProfessionSerializer,
    WarriorSkillsSerializer,
    WarriorFullSerializer,
    WarriorCreateUpdateSerializer,
)


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionCreateSerializer(data=profession)
        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()
        return Response(
            {
                "Success": "Profession '{}' created succesfully.".format(
                    profession_saved.title
                )
            }
        )


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
            return Response(
                {"Success": f"Skill '{skill_saved.title}' created successfully."}
            )


class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.select_related('profession').all()


class WarriorSkillsListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillsSerializer
    queryset = Warrior.objects.prefetch_related('skillofwarrior_set__skill').all()


class WarriorDetailAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorFullSerializer
    queryset = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()


class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorCreateUpdateSerializer


class WarriorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WarriorFullSerializer
        return WarriorCreateUpdateSerializer
