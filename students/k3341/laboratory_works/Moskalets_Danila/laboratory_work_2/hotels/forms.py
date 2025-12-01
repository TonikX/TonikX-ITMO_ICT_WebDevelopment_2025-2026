from django import forms
from .models import Reservation, Review
from django.core.exceptions import ValidationError
from datetime import date


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

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            today = date.today()

            if check_in < today:
                raise ValidationError({
                    'check_in': f'Дата заезда ({check_in}) не может быть в прошлом! Сегодня {today.strftime("%d.%m.%Y")}.'
                })

            if check_out <= check_in:
                raise ValidationError({
                    'check_out': f'Дата выезда ({check_out}) должна быть ПОСЛЕ даты заезда ({check_in}).'
                })

            if self.room_type:
                conflicting_reservations = Reservation.objects.filter(
                    room_type=self.room_type,
                    status__in=['pending', 'confirmed', 'checked_in'],
                    check_in__lt=check_out,
                    check_out__gt=check_in
                )

                if self.instance:
                    conflicting_reservations = conflicting_reservations.exclude(id=self.instance.id)

                if conflicting_reservations.exists():
                    occupied_periods = []
                    for reservation in conflicting_reservations:
                        occupied_periods.append(
                            f"{reservation.check_in.strftime('%d.%m.%Y')} - {reservation.check_out.strftime('%d.%m.%Y')}"
                        )

                    error_message = (
                            f'На выбранные даты ({check_in.strftime("%d.%m.%Y")} - {check_out.strftime("%d.%m.%Y")}) номер уже забронирован.\n'
                            'Занятые периоды:\n' +
                            '\n'.join([f'• {period}' for period in occupied_periods]) +
                            '\n\nПожалуйста, выберите другие даты.'
                    )

                    raise ValidationError({
                        'check_in': error_message,
                        'check_out': error_message
                    })

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Напишите ваш отзыв...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control', 'placeholder': '1-10'}),
        }
        labels = {
            'text': 'Текст отзыва',
            'rating': 'Рейтинг (1-10)',
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 10):
            raise ValidationError('Рейтинг должен быть от 1 до 10')
        return rating