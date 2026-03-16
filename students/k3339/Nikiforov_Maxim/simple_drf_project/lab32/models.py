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
	RACE_CHOICES = (
		('s', 'student'),
		('d', 'developer'),
		('t', 'teamlead'),
	)
	race = models.CharField(max_length=1, choices=RACE_CHOICES, verbose_name='Раса')
	name = models.CharField(max_length=120, verbose_name='Имя')
	level = models.IntegerField(verbose_name='Уровень', default=0)
	profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Профессия', related_name='warriors')
	skill = models.ManyToManyField(Skill, through='SkillOfWarrior', verbose_name='Умения', related_name='warriors')

	def __str__(self):
		return self.name


class SkillOfWarrior(models.Model):
	skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name='Умение')
	warrior = models.ForeignKey(Warrior, on_delete=models.CASCADE, verbose_name='Воин', related_name='warrior_skills')
	level = models.IntegerField(verbose_name='Уровень освоения умения')

	def __str__(self):
		return f"{self.warrior.name} - {self.skill.title}"
