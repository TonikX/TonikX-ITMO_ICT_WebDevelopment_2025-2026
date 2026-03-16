"""
Формы для приложения racing.
"""
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import DriverProfile, Registration, Comment


class DriverProfileForm(forms.ModelForm):
    """Форма для редактирования профиля водителя."""
    
    class Meta:
        model = DriverProfile
        fields = ['full_name', 'car_description', 'bio', 'experience_years', 'driver_class', 'team']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем полное имя обязательным
        self.fields['full_name'].required = True
        self.fields['full_name'].help_text = 'Обязательное поле. Укажите ваше полное имя.'
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))
    
    def clean_full_name(self):
        """Валидация полного имени."""
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not full_name:
            raise forms.ValidationError('Пожалуйста, укажите ваше полное имя.')
        if len(full_name) < 2:
            raise forms.ValidationError('Полное имя должно содержать минимум 2 символа.')
        return full_name


class RegistrationForm(forms.ModelForm):
    """Форма для регистрации на гонку."""
    
    class Meta:
        model = Registration
        fields = ['car_number']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car_number'].required = False
        self.fields['car_number'].label = 'Номер машины (необязательно)'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))


class CommentForm(forms.ModelForm):
    """Форма для добавления комментария к гонке."""
    
    class Meta:
        model = Comment
        fields = ['heat_date', 'kind', 'rating', 'text']
        widgets = {
            'heat_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем формат даты для правильного отображения при редактировании
        self.fields['heat_date'].input_formats = ['%Y-%m-%d']
        self.fields['heat_date'].widget.format = '%Y-%m-%d'
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отправить комментарий'))
        
    def clean_rating(self):
        """Валидация рейтинга."""
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 10):
            raise ValidationError('Рейтинг должен быть от 1 до 10.')
        return rating

