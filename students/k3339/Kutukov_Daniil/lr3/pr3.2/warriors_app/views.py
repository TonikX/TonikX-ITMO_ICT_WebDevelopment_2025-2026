from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import (
    WarriorSerializer,
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    WarriorDetailSerializer,
    WarriorCreateSerializer,
    ProfessionSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    SkillCreateSerializer,
)


# ============================================================================
# APIView примеры (для первого практического задания)
# ============================================================================


class WarriorAPIView(APIView):
    """Просмотр всех воинов через APIView"""

    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):
    """Создание профессии через APIView"""

    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionCreateSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response(
            {"Success": f"Profession '{profession_saved.title}' created successfully."}
        )


class SkillAPIView(APIView):
    """Просмотр всех умений через APIView (Практическое задание 1)"""

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateAPIView(APIView):
    """Создание умения через APIView (Практическое задание 1)"""

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response(
            {"Success": f"Skill '{skill_saved.title}' created successfully."}
        )


# ============================================================================
# Generic Views (для второго практического задания)
# ============================================================================


class WarriorListAPIView(generics.ListAPIView):
    """Список всех воинов через Generic View"""

    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class ProfessionCreateAPIView(generics.CreateAPIView):
    """Создание профессии через Generic View"""

    serializer_class = ProfessionCreateSerializer
    queryset = Profession.objects.all()


class SkillListAPIView(generics.ListAPIView):
    """Список всех умений через Generic View"""

    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class SkillCreateGenericAPIView(generics.CreateAPIView):
    """Создание умения через Generic View"""

    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


# ============================================================================
# Generic Views для практического задания (с вложенными данными)
# ============================================================================


class WarriorWithProfessionListAPIView(generics.ListAPIView):
    """
    Вывод полной информации о всех воинах и их профессиях
    (Практическое задание: пункт 1)
    """

    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.select_related("profession").all()


class WarriorWithSkillsListAPIView(generics.ListAPIView):
    """
    Вывод полной информации о всех воинах и их скилах
    (Практическое задание: пункт 2)
    """

    serializer_class = WarriorSkillSerializer
    queryset = Warrior.objects.prefetch_related("skill").all()


class WarriorDetailAPIView(generics.RetrieveAPIView):
    """
    Вывод полной информации о воине (по id), его профессии и скилах
    (Практическое задание: пункт 3)
    """

    serializer_class = WarriorDetailSerializer
    queryset = (
        Warrior.objects.select_related("profession").prefetch_related("skill").all()
    )


class WarriorDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление воина по id
    (Практическое задание: пункт 4)
    """

    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование информации о воине
    (Практическое задание: пункт 5)
    """

    serializer_class = WarriorCreateSerializer
    queryset = Warrior.objects.all()


class WarriorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Комбинированный view для получения, обновления и удаления воина
    (Бонус: все операции в одном endpoint)
    """

    serializer_class = WarriorDetailSerializer
    queryset = (
        Warrior.objects.select_related("profession").prefetch_related("skill").all()
    )
