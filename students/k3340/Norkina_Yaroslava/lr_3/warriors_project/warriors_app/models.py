from django.db import models

class Profession(models.Model):

    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"


class Skill(models.Model):

    title = models.CharField(max_length=120, verbose_name='Наименование')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Умение"
        verbose_name_plural = "Умения"


class Warrior(models.Model):

    race_types = (
        ('s', 'student'),
        ('d', 'developer'),
        ('t', 'teamlead'),
    )
    race = models.CharField(max_length=1, choices=race_types, verbose_name='Расса')
    name = models.CharField(max_length=120, verbose_name='Имя')
    level = models.IntegerField(verbose_name='Уровень', default=0)
    skill = models.ManyToManyField(
        'Skill',
        verbose_name='Умения',
        through='SkillOfWarrior',
        related_name='warrior_skills'
    )
    profession = models.ForeignKey(
        'Profession',
        on_delete=models.CASCADE,
        verbose_name='Профессия',
        blank=True,
        null=True,
        related_name='warriors'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Воин"
        verbose_name_plural = "Воины"


class SkillOfWarrior(models.Model):

    skill = models.ForeignKey(
        'Skill',
        verbose_name='Умение',
        on_delete=models.CASCADE,
        related_name='skill_of_warriors'
    )
    warrior = models.ForeignKey(
        'Warrior',
        verbose_name='Воин',
        on_delete=models.CASCADE,
        related_name='skills'
    )
    level = models.IntegerField(verbose_name='Уровень освоения умения')

    def __str__(self):
        return f"{self.warrior.name} - {self.skill.title} (уровень {self.level})"

    class Meta:
        verbose_name = "Умение воина"
        verbose_name_plural = "Умения воинов"