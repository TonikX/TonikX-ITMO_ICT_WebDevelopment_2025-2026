from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Warrior,
    Profession,
    Skill,
)
from .serializers import (
    WarriorSerializer,
    WarriorUpdateSerializer,
    ProfessionSerializer,
    SkillSerializer,
    WarriorProfessionSerializer,
    WarriorSkillsSerializer,
    WarriorProfessionSkillsSerializer,
)


# ===== Warrior =====

class WarriorListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorCreateAPIView(generics.CreateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer 


class WarriorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorUpdateSerializer


class WarriorDestroyAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


# ===== Profession =====

class ProfessionListAPIView(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class ProfessionCreateAPIView(generics.CreateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer 


class ProfessionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class ProfessionUpdateAPIView(generics.UpdateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class ProfessionDestroyAPIView(generics.DestroyAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


# ===== Skill =====

# Реализация более примитивным методом
# (согласно заданию)
class SkillListAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


# Реализация более примитивным методом
# (согласно заданию)
class SkillCreateAPIView(APIView):
    def post(self, request):
       skill = request.data
       serializer = SkillSerializer(data=skill)
       if serializer.is_valid(raise_exception=True):
           skill_saved = serializer.save()
       return Response({"Success": "Skill '{}' created successfully.".format(skill_saved.title)})


class SkillRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillUpdateAPIView(generics.UpdateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillDestroyAPIView(generics.DestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


# ===== Специальные запросы =====

# Вывод полной информации о всех воинах и их профессиях
class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.all().select_related('profession')


# Вывод полной информации о всех воинах и их навыках
class WarriorSkillsListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillsSerializer
    queryset = Warrior.objects.all().prefetch_related('skillofwarrior_set__skill')

# Вывод полной информации воине, его профессии и навыках
class WarriorProfessionSkillsAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorProfessionSkillsSerializer
    queryset = (
        Warrior.objects.all()
        .select_related('profession')
        .prefetch_related('skillofwarrior_set__skill')
    )
