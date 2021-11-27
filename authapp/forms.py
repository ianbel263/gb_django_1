from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from authapp.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'

        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    age = forms.IntegerField(widget=forms.NumberInput(), required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'image',
            'username',
            'email',
            'age'
        ]

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['image'].label = 'Выберите изображение'
        self.fields['age'].label = 'Возраст'

        # self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        # self.fields['email'].widget.attrs['placeholder'] = 'Введите e-mail'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['image'].widget.attrs['placeholder'] = 'Выберите изображение'
        self.fields['age'].widget.attrs['placeholder'] = 'Введите Ваш возраст'

        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите e-mail'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'
