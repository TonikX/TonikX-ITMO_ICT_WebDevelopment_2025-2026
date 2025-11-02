from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reservation, Review, Room, RoomType
from datetime import date, timedelta

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        }),
        label="Email адрес"
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Придумайте имя пользователя'
        }),
        label="Имя пользователя",
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_."
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        label="Пароль",
        help_text="""
        <ul>
            <li>Пароль не должен быть слишком похож на другую вашу личную информацию.</li>
            <li>Пароль должен содержать как минимум 8 символов.</li>
            <li>Пароль не может состоять только из цифр.</li>
        </ul>
        """
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        }),
        label="Подтверждение пароля",
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = self.fields['password1'].help_text
        self.fields['password2'].help_text = self.fields['password2'].help_text


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.room_type = kwargs.pop('room_type', None)
        super().__init__(*args, **kwargs)

    def clean_check_in(self):
        check_in = self.cleaned_data.get('check_in')
        if check_in and check_in < date.today():
            self.add_error('check_out', "Дата заезда не может быть раньше сегодняшнего дня.")
        return check_in

    def clean_check_out(self):
        check_out = self.cleaned_data.get('check_out')
        if check_out and check_out <= date.today():
            self.add_error('check_out', "Дата выезда не может быть раньше сегодняшнего дня.")
        return check_out
    
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_out <= check_in:
                self.add_error('check_out', "Дата выезда должна быть позже даты заезда (минимум 1 ночь).")
        
        if check_in and check_out and self.room_type:
            available_room = None
            for room in Room.objects.filter(type=self.room_type):
                if room.is_available(check_in, check_out):
                    available_room = room
                    break
            
            if not available_room:
                raise forms.ValidationError(
                    "❌ К сожалению, нет свободных номеров на выбранные даты. "
                    "Пожалуйста, выберите другие даты."
                )
            
            cleaned_data['available_room'] = available_room
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if hasattr(self, 'cleaned_data') and 'available_room' in self.cleaned_data:
            instance.room = self.cleaned_data['available_room']
        
        if commit:
            instance.save()
        return instance
    

class EditReservationForm(forms.ModelForm):
    new_room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="🛏️ Тип номера",
        required=True,
        empty_label="Оставить текущий тип"
    )
    
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.reservation = kwargs.pop('reservation', None)
        super().__init__(*args, **kwargs)
        
        if self.reservation:
            hotel = self.reservation.room.type.hotel
            self.fields['new_room_type'].queryset = RoomType.objects.filter(hotel=hotel)
            self.fields['new_room_type'].initial = self.reservation.room.type
    
    def clean_check_in(self):
        check_in = self.cleaned_data.get('check_in')
        if check_in and check_in < date.today():
            self.add_error('check_out', "Дата заезда не может быть раньше сегодняшнего дня.")
        return check_in

    def clean_check_out(self):
        check_out = self.cleaned_data.get('check_out')
        if check_out and check_out <= date.today():
            self.add_error('check_out', "Дата выезда не может быть раньше сегодняшнего дня.")
        return check_out
    
    def clean(self):
        cleaned_data = super().clean()
        new_room_type = cleaned_data.get('new_room_type')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_out <= check_in:
                self.add_error('check_out', "Дата выезда должна быть позже даты заезда (минимум 1 ночь).")
        
        if all([new_room_type, check_in, check_out, self.reservation]):
            available_room = None
            for room in new_room_type.room_set.all():
                if room.is_available(check_in, check_out, exclude_reservation=self.reservation):
                    available_room = room
                    break

            if not available_room:
                self.add_error('new_room_type', 
                    f"В типе номера '{new_room_type.name}' нет свободных комнат на выбранные даты."
                )

            cleaned_data['new_room'] = available_room

        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'new_room' in self.cleaned_data:
            instance.room = self.cleaned_data['new_room']
        
        if commit:
            instance.save()
        return instance


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(),
        label="",
        help_text="Выберите оценку от 1 (ужасно) до 10 (прекрасно)"
    )
    
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Расскажите о вашем опыте проживания...'
        }),
        label="Текст отзыва",
        max_length=2000
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating:
            rating = int(rating)
            if rating < 1 or rating > 10:
                raise ValidationError("Рейтинг должен быть от 1 до 10.")
        return rating
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment and len(comment.strip()) < 10:
            raise ValidationError("Отзыв должен содержать не менее 10 символов.")
        return comment
