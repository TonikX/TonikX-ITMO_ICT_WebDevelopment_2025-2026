"""
Формы для админки приложения racing.
"""
from django import forms
from .models import HeatResult, Registration


class HeatResultAdminForm(forms.ModelForm):
    """Форма для результата заезда в админке с ограничением водителей."""
    
    class Meta:
        model = HeatResult
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Если заезд уже выбран (редактирование существующего результата)
        if self.instance and self.instance.heat_id:
            heat = self.instance.heat
            # Ограничиваем выбор водителей только зарегистрированными на эту гонку
            registered_drivers = Registration.objects.filter(
                race=heat.race,
                active=True
            ).values_list('driver_id', flat=True)
            
            self.fields['driver'].queryset = self.fields['driver'].queryset.filter(
                id__in=registered_drivers
            )
            self.fields['driver'].help_text = f'Только водители, зарегистрированные на гонку "{heat.race.title}"'
        
        # Если это создание нового результата через инлайн, ограничение применится через JS
        # или после выбора заезда

