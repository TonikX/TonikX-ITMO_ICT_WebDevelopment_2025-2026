from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from .models import Warrior, Profession, Skill
from .serializers import (
    WarriorSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    ProfessionSerializer,
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    WarriorNestedSerializer,
)

# Просмотр всех скиллов
class SkillListAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"skills": serializer.data})


# Создание нового скилла
class SkillCreateAPIView(APIView):
    def get(self, request):
        # просто вернём текущий список скиллов,
        # чтобы DRF мог отрисовать страницу и форму POST
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"skills": serializer.data})

    def post(self, request):
        # ожидаем, что в теле запроса придет объект {"skill": {"title": "Python"}}
        skill_data = request.data.get("skill")

        serializer = SkillSerializer(data=skill_data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
            return Response({"Success": f"Skill '{skill_saved.title}' created successfully."})


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

       return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class WarriorProfessionListAPIView(ListAPIView):
    """
    Вывод полной информации о всех воинах и их профессиях
    (в одном запросе).
    """
    queryset = Warrior.objects.select_related('profession').all()
    serializer_class = WarriorProfessionSerializer


class WarriorSkillListAPIView(ListAPIView):
    """
    Вывод полной информации о всех воинах и их скиллах (в одном запросе).
    """
    queryset = Warrior.objects.prefetch_related('skill').all()
    serializer_class = WarriorSkillSerializer


class WarriorFullDetailView(RetrieveAPIView):
    """
    Пункт 3:
    Вывод полной информации о войне (по id), его профессии и скилах.
    """
    queryset = Warrior.objects.select_related("profession").prefetch_related("skill").all()
    serializer_class = WarriorNestedSerializer
    lookup_field = "id"   # можно "pk", если тебе так привычнее


class WarriorDeleteView(DestroyAPIView):
    """
    Пункт 4:
    Удаление воина по id.
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = "id"


class WarriorUpdateView(UpdateAPIView):
    """
    Пункт 5:
    Редактирование информации о войне.
    """
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = "id"
