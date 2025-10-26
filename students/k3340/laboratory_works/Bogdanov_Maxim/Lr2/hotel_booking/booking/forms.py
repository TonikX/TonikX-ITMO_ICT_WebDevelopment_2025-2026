from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Booking, Review, RoomType, Amenity, Room
from .services import check_room_availability, calculate_booking_price
from datetime import date


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        hotel_id = kwargs.pop('hotel_id', None)
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            queryset = Room.objects.filter(is_active=True)

            if hotel_id:
                queryset = queryset.filter(room_type__hotel_id=hotel_id)

            self.fields['room'].queryset = queryset.select_related('room_type__hotel')

    def clean_check_in(self):
        check_in = self.cleaned_data.get('check_in')
        if not self.instance.pk and check_in and check_in < date.today():
            raise ValidationError('Дата заезда не может быть в прошлом')
        return check_in

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')

        if check_in and check_out:
            if check_in >= check_out:
                raise ValidationError('Дата выезда должна быть позже даты заезда')

            if room:
                exclude_id = self.instance.pk if self.instance.pk else None
                if not check_room_availability(room, check_in, check_out, exclude_id):
                    raise ValidationError('Номер недоступен на выбранные даты')

        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)

        if not booking.pk:
            booking.user = self.user
            booking.status = 'pending'

        if booking.check_in and booking.check_out:
            booking.total_price = calculate_booking_price(
                booking.room,
                booking.check_in,
                booking.check_out
            )

        if commit:
            booking.save()

        return booking


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.booking = kwargs.pop('booking', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if self.booking:
            if self.booking.check_in > date.today():
                raise ValidationError('Отзыв можно оставить только после заезда')

            if self.booking.status not in ['checked_in', 'checked_out']:
                raise ValidationError('Отзыв можно оставить только для подтверждённых бронирований')

            if not self.instance.pk:
                existing_review = Review.objects.filter(
                    booking=self.booking,
                    user=self.user
                ).exists()

                if existing_review:
                    raise ValidationError('Вы уже оставили отзыв на это бронирование')

        return cleaned_data

    def save(self, commit=True):
        review = super().save(commit=False)
        review.user = self.user
        review.booking = self.booking
        review.room = self.booking.room
        review.stay_start = self.booking.check_in
        review.stay_end = self.booking.check_out

        if commit:
            review.save()

        return review


class HotelFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию или адресу', 'class': 'form-control'})
    )


class RoomFilterForm(forms.Form):
    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.all(),
        required=False,
        empty_label='Все типы',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    min_capacity = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Мин. вместимость', 'class': 'form-control'})
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Макс. цена за ночь', 'class': 'form-control'})
    )
    check_in = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    check_out = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        hotel_id = kwargs.pop('hotel_id', None)
        super().__init__(*args, **kwargs)

        if hotel_id:
            self.fields['room_type'].queryset = RoomType.objects.filter(hotel_id=hotel_id)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_in >= check_out:
            raise ValidationError('Дата выезда должна быть позже даты заезда')

        return cleaned_data