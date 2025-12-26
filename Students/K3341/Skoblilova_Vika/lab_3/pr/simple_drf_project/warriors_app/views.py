from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Warrior
from .serializers import (
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    WarriorDetailSerializer,
    WarriorUpdateSerializer
)

class WarriorProfessionAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorProfessionSerializer(warriors, many=True)
        return Response({"warriors": serializer.data})

class WarriorSkillAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorSkillSerializer(warriors, many=True)
        return Response({"warriors": serializer.data})

class WarriorDetailAPIView(APIView):
    def get(self, request, pk):
        warrior = get_object_or_404(
            Warrior.objects.select_related('profession')
                          .prefetch_related('warrior_skills__skill'),
            pk=pk
        )
        serializer = WarriorDetailSerializer(warrior)
        return Response(serializer.data)

class WarriorDeleteAPIView(APIView):
    def delete(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        warrior_name = warrior.name
        warrior.delete()
        return Response(
            {"success": f"Воин '{warrior_name}' удален"},
            status=status.HTTP_204_NO_CONTENT
        )

class WarriorUpdateAPIView(APIView):
    def put(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorUpdateSerializer(warrior, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "Информация обновлена", "warrior": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)