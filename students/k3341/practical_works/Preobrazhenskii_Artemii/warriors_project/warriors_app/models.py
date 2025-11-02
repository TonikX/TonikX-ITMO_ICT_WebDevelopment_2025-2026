from django.db import models


class Profession(models.Model):
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Skill(models.Model):
    title = models.CharField(max_length=120, verbose_name='Наименование')

    def __str__(self):
        return self.title


class Warrior(models.Model):
    race_types = (
        ('s', 'student'),
        ('d', 'developer'),
        ('t', 'teamlead'),
    )
    race = models.CharField(max_length=1, choices=race_types, verbose_name='Расса')
    name = models.CharField(max_length=120, verbose_name='Имя')
    level = models.IntegerField(verbose_name='Уровень', default=0)
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, verbose_name='Профессия', blank=True, null=True
    )
    skill = models.ManyToManyField(Skill, through='SkillOfWarrior', related_name='warrior_skills')

    def __str__(self):
        return self.name


class SkillOfWarrior(models.Model):
    warrior = models.ForeignKey(Warrior, on_delete=models.CASCADE, verbose_name='Воин')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name='Умение')
    level = models.IntegerField(verbose_name='Уровень освоения умения')

    def __str__(self):
        return f"{self.warrior.name} - {self.skill.title} ({self.level})"