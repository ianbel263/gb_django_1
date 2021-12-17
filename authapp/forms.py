import hashlib
from random import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authapp.models import User, UserProfile
from authapp.validate import validate_age


def update_widgets(fields):
    labels = {
        'first_name': _('Name'),
        'last_name': _('Surname'),
        'image': _('Upload avatar'),
        'username': _('Username'),
        'email': _('Email'),
        'age': _('Age'),
        'password': _('Password'),
        'password1': _('Password'),
        'password2': _('Confirm password'),
        'about': _('About yourself'),
        'gender': _('Gender')
    }

    placeholders = {
        'first_name': _('Enter name'),
        'last_name': _('Enter surname'),
        'image': _('Upload avatar'),
        'username': _('Enter username'),
        'email': _('Enter e-mail'),
        'age': _('Enter your age'),
        'password': _('Enter password'),
        'password1': _('Enter password'),
        'password2': _('Confirm password'),
        'about': _('Tell about yourself'),
        'gender': _('Gender')
    }

    for name, field in fields.items():
        if name == 'image':
            field.widget.attrs['class'] = 'custom-file-input'
        elif name == 'gender' or name == 'age':
            field.widget.attrs['class'] = 'form-control'
        else:
            field.widget.attrs['class'] = 'form-control py-4'
        if name in labels:
            field.label = labels[name]
        if name in placeholders:
            field.widget.attrs['placeholder'] = placeholders[name]


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        update_widgets(self.fields)

    def get_invalid_login_error(self):
        user = User.objects.get(username=self.cleaned_data.get('username'))
        if user and not user.is_active:
            return ValidationError(
                self.error_messages['inactive'],
                code='inactive', )
        else:
            return ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}, )


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    age = forms.IntegerField(widget=forms.NumberInput(), required=False, validators=[validate_age])

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'username',
            'email',
            'age',
        )

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['first_name'].widget.attrs['autofocus'] = True
        update_widgets(self.fields)


class UserAdditionalProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(UserAdditionalProfileForm, self).__init__(*args, **kwargs)
        update_widgets(self.fields)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
        update_widgets(self.fields)

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user
