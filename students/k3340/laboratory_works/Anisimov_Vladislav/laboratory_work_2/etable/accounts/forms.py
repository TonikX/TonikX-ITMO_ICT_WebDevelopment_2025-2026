from django import forms
from django.contrib.auth import authenticate
from .models import User

class UserRegisterForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        widget=forms.Select(attrs={'placeholder': 'Выберите тип пользователя', 'class':"form-group"}),
        label="Тип пользователя",
        error_messages={'required': 'Выберите тип пользователя'},
        choices=[('student', 'Ученик'), ('teacher', 'Учитель'),],
    )
    username = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя', 'class':"form-group"}),
        label="Имя пользователя",
        error_messages={'required': 'Введите имя пользователя'}
    )
    full_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ФИО', 'class':"form-group"}),
        label="ФИО",
        error_messages={'required': 'Введите ФИО'}
    )    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class':"form-group"}),
        label="Пароль",
        error_messages={'required': 'Введите пароль'}
    )
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль', 'class':"form-group"}),
        label="Пароль ещё раз",
        error_messages={'required': 'Повторите пароль'}
    )
    class Meta():
        model = User
        fields = ['user_type', 'full_name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        full_name = cleaned_data.get("full_name")
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if not username:
            self.add_error('username', "Введите имя пользователя")
        if not password:
            self.add_error('password', "Введите пароль")

        if password and password_repeat and password != password_repeat:
            self.add_error('password_repeat', "Пароли не совпадают")

        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя', 'class':"form-group"}),
        label="Имя пользователя",
        error_messages={'required': 'Введите имя пользователя'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class':"form-group"}),
        label="Пароль",
        error_messages={'required': 'Введите пароль'}
    )
    
    class Meta():
        model = User
        fields = ['username', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            #user = authenticate(username=username, password=password)
            user = User.objects.filter(username=username).first()
            if not user or not user.check_password(password):
                self.add_error(None, "Неправильный логин или пароль")
            self.user = user 
        else:
            #self.add_error('username', "Пользователь не найден")
            self.user = None

        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)