from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Warrior, Profession, Skill
from .serializers import WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, WarriorDetailSerializer, \
    WarriorCreateSerializer, WarriorDetailSkillsSerializer, WarriorFullSerializer


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})

    def post(self, request):
        warrior = request.data
        serializer = WarriorCreateSerializer(data=warrior)
        if serializer.is_valid(raise_exception=True):
            warrior_saved = serializer.save()

        return Response({"Success": "Warrior '{}' created succesfully.".format(warrior_saved.name)})


class ProfessionCreateView(APIView):
    def get(self, request):
        professions = Profession.objects.all()
        serializer = ProfessionCreateSerializer(professions, many=True)
        return Response({"Professions": serializer.data})

    def post(self, request):
        profession = request.data
        serializer = ProfessionCreateSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    def post(self, request):
        skill = request.data
        serializer = SkillSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Succes": "Skill '{}' created succesfully.".format(skill_saved.title)})


class WarriorProfessions(APIView):
    def get(self, request):
        warrior = Warrior.objects.select_related('profession').all()
        serializer = WarriorDetailSerializer(warrior, many=True)
        return Response(serializer.data)


class WarriorSkills(APIView):
    def get(self, request):
        warrior = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorDetailSkillsSerializer(warrior, many=True)
        return Response(serializer.data)


class WarriorPK(APIView):
    def get(self, request, pk):
        warrior = Warrior.objects.filter(id=pk).first()
        serializer = WarriorFullSerializer(warrior)
        return Response(serializer.data)

    def delete(self, request, pk):
        warrior = Warrior.objects.filter(id=pk).first()
        if not warrior:
            return Response({"success": False, "error": f"Воин с ID {pk} не найден"})

        warrior_data = {'id': warrior.id, 'name': warrior.name}
        warrior.delete()
        return Response({"Succes": True, "message": f'Воин "{warrior_data["name"]}" (ID: {warrior_data["id"]}) успешно удален'})

    def patch(self, request, pk):
        warrior = Warrior.objects.filter(id=pk).first()
        if not warrior:
            return Response({"success": False, "error": f"Воин с ID {pk} не найден"})

        serializer = WarriorSerializer(warrior, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Данные воина успешно обновлены", "data": serializer.data})