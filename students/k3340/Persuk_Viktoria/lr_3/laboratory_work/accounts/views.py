from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from .models import Profile
from .serializers import ProfileSerializer


User = get_user_model()


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Возвращает / обновляет профиль для текущего авторизованного пользователя.

    Эндпоинт: GET/PATCH /api/profile/
    """

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        """
        Возвращает профиль для текущего авторизованного пользователя.
        """
        profile, _ = Profile.objects.select_related("user").get_or_create(
            user=self.request.user
        )
        return profile


    def perform_update(self, serializer):
        """
        Обновляет профиль для текущего авторизованного пользователя.
        """
        serializer.save(user=self.request.user)


class UserProfileDetailView(generics.RetrieveAPIView):
    """
    Только для чтения доступ к профилю другого пользователя.

    Эндпоинт: GET /api/users/<id>/profile/
    """

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "user_id"


    def get_object(self):
        """
        Возвращает профиль для другого пользователя.
        """
        user_id = self.kwargs[self.lookup_url_kwarg]
        return get_object_or_404(
            Profile.objects.select_related("user"), user__id=user_id
        )
