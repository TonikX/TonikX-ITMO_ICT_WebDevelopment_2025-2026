from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior


# Уходим от ручного создания полей и используем наследование класса сериализатора от
# ModelSerializer, для которого достаточно указать лишь название модели и требуемые поля
class ProfessionSerializer(serializers.ModelSerializer):
    
    # Автоматически создаваемые поля. Поля сериалайзера, 
    # имена которых указаны во внутреннем классе Meta явно через fields
    class Meta:
        model = Profession
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Skill
        fields = '__all__'


class SkillOfWarriorSerializer(serializers.ModelSerializer):

    # Декларируемые поля - обычные поля сериалайзера, которые мы описываем самостоятельно 
    # вне класса Meta. Зачем? названия полей модели и сериализатора не совпадают
    # 'Skill' vs skill
    
    skill = SkillSerializer(read_only=True) 
    
    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'skill', 'level']


class WarriorSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Warrior
        fields = '__all__'


class WarriorProfessionSerializer(serializers.ModelSerializer):
    
    profession = ProfessionSerializer(read_only=True)
    # source для переопределения значения поля: поле race, в котором в качестве аргумента source 
    # был передан метод get_race_display, необходимый для того, чтобы вытащить значение из choices,
    # а не возвращать только ключ.

    race = serializers.CharField(source='get_race_display', read_only=True)
    
    class Meta:
        model = Warrior
        fields = '__all__'


class WarriorSkillsSerializer(serializers.ModelSerializer):

    # зачем тут source?
    # Указывая many=True, мы включаем логику обработки набора записей.
    skill = SkillOfWarriorSerializer(source='skills', many=True, read_only=True) # ????
    race = serializers.CharField(source='get_race_display', read_only=True)
    
    class Meta:
        model = Warrior
        fields = '__all__'


class WarriorFullSerializer(serializers.ModelSerializer):
    
    profession = ProfessionSerializer(read_only=True)
    skill = SkillOfWarriorSerializer(source='skills', many=True, read_only=True) # зачем тут source?
    race = serializers.CharField(source='get_race_display', read_only=True)
    
    class Meta:
        model = Warrior
        fields = '__all__'


class WarriorCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Warrior
        fields = '__all__'


class ProfessionCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profession
        fields = '__all__'


class SkillCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Skill
        fields = '__all__'


class SkillOfWarriorCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkillOfWarrior
        fields = '__all__'