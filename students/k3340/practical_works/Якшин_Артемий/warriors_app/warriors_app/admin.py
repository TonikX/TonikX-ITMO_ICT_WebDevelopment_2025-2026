from django.contrib import admin
from .models import Warrior, Profession, Skill, SkillOfWarrior


@admin.register(Warrior)
class WarriorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'race', 'level', 'profession')
    list_filter = ('race', 'level', 'profession')
    search_fields = ('name',)


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(SkillOfWarrior)
class SkillOfWarriorAdmin(admin.ModelAdmin):
    list_display = ('id', 'warrior', 'skill', 'level')
    list_filter = ('level',)
