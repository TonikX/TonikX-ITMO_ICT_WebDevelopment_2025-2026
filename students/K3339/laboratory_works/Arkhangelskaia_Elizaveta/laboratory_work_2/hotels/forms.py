from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HotelUser, Reservation, RoomType

class HotelUserCreationForm(UserCreationForm):
    class Meta:
        model = HotelUser
        fields = ('username', 'first_name', 'last_name', 'birth_date',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['birth_date'].label = "Дата рождения"
        self.fields['email'].label = "Электронная почта"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"
        for field in self.fields.values():
            field.help_text = None


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'num_of_people']


    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        checkin = cleaned_data.get('start_date')
        checkout = cleaned_data.get('end_date')
        num_of_people = cleaned_data.get('num_of_people')

        if checkin and checkout:
            if checkout <= checkin:
                raise forms.ValidationError('Дата выезда должна быть позже даты заезда')

        if num_of_people is not None:
            if num_of_people <= 0:
                raise forms.ValidationError('Количество гостей должно быть больше нуля')
            if self.room and num_of_people:
                if num_of_people > self.room.capacity:
                    raise forms.ValidationError(
                        f"Количество гостей не должно превышать {self.room.capacity} для этой комнаты")

        return cleaned_data