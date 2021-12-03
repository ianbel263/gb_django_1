from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authapp.models import User


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
        'password2': _('Confirm password')
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
        'password2': _('Confirm password')
    }

    for name, field in fields.items():
        if name == 'image':
            field.widget.attrs['class'] = 'custom-file-input'
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


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    age = forms.IntegerField(widget=forms.NumberInput(), required=False)

    error_messages = {
        'age_mismatch': _('The age must be at least 18 years old.'),
    }

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
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['first_name'].widget.attrs['autofocus'] = True
        update_widgets(self.fields)

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise ValidationError(
                self.error_messages['age_mismatch'],
                code='age_mismatch'
            )
        return age


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
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
        update_widgets(self.fields)
