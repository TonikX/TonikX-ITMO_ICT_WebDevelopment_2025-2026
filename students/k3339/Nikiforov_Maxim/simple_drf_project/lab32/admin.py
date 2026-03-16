from django.contrib import admin
from .models import Skill, Profession, Warrior, SkillOfWarrior


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	list_display = ('id', 'title')
	search_fields = ('title',)


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'title')
	search_fields = ('title',)


@admin.register(Warrior)
class WarriorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'race', 'level', 'profession')
	list_filter = ('race', 'level')
	search_fields = ('name',)


@admin.register(SkillOfWarrior)
class SkillOfWarriorAdmin(admin.ModelAdmin):
	list_display = ('warrior', 'skill', 'level')
	list_filter = ('warrior', 'skill')
	search_fields = ('warrior__name', 'skill__title')
