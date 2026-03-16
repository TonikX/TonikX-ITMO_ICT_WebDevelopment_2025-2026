from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .models import Skill, Warrior, Profession
from .serializers import (
	SkillSerializer, WarriorSerializer, ProfessionSerializer,
	WarriorWithProfessionSerializer, WarriorWithSkillsSerializer,
	WarriorDetailSerializer
)


class SkillAPIView(APIView):
	def get(self, request):
		skills = Skill.objects.all()
		serializer = SkillSerializer(skills, many=True)
		return Response({"skills": serializer.data})

	def post(self, request):
		serializer = SkillSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			skill = serializer.save()
			return Response({"success": f"Skill '{skill.title}' created successfully."}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 1. Get all warriors with professions
class WarriorListWithProfessionAPIView(generics.ListAPIView):
	serializer_class = WarriorWithProfessionSerializer
	queryset = Warrior.objects.all()


# 2. Get all warriors with skills
class WarriorListWithSkillsAPIView(generics.ListAPIView):
	serializer_class = WarriorWithSkillsSerializer
	queryset = Warrior.objects.all()


# 3. Get specific warrior by id with professions and skills
class WarriorDetailAPIView(generics.RetrieveAPIView):
	serializer_class = WarriorDetailSerializer
	queryset = Warrior.objects.all()


# 4. Delete warrior by id
class WarriorDestroyAPIView(generics.DestroyAPIView):
	serializer_class = WarriorSerializer
	queryset = Warrior.objects.all()


# 5. Edit warrior information
class WarriorUpdateAPIView(generics.UpdateAPIView):
	serializer_class = WarriorSerializer
	queryset = Warrior.objects.all()
