from django.db import models
from django.conf import settings
from races.models import Race


class Comment(models.Model):
    COMMENT_TYPES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('racing', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name='Гонка')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    comment_type = models.CharField(
        max_length=20,
        choices=COMMENT_TYPES,
        verbose_name='Тип комментария'
    )
    text = models.TextField(verbose_name='Текст комментария')
    rating = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        choices=[(i, i) for i in range(1, 11)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    race_date = models.DateField(verbose_name='Дата заезда')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от {self.author} к {self.race}"