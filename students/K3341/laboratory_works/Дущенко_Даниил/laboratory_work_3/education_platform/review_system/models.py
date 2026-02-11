from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание задания")
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self):
        return self.title


class Variant(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='variants')
    option_number = models.PositiveIntegerField("Номер варианта")
    description = models.TextField("Текст варианта")

    def __str__(self):
        return f"{self.assignment.title} - Вар. {self.option_number}"


class GradingCriterion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='criteria')
    name = models.CharField("Название критерия", max_length=200)
    max_score = models.PositiveIntegerField("Макс. балл")

    def __str__(self):
        return self.name


class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    content = models.TextField("Текст решения или ссылка")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Решение от {self.student.username}"


class PeerReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reviews_received')
    comments = models.TextField("Комментарий проверяющего")
    total_score = models.PositiveIntegerField("Итоговый балл", default=0)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Проверка {self.reviewer.username} -> {self.submission.student.username}"