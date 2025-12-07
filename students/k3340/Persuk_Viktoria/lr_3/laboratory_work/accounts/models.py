from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Дополнительная информация о пользователе

    Пользователь хранится в стандартной модели User (Djoser),
    здесь только расширение профиля
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )

    display_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Отображаемое имя",
        help_text="Если не заполнено — можно использовать username из User",
    )

    bio = models.TextField(
        blank=True,
        verbose_name="О себе",
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")


    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


    def __str__(self) -> str:
        return self.display_name or f"Профиль пользователя {self.user}"
