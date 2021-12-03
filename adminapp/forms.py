from django import forms

from authapp.forms import UserRegisterForm
from authapp.models import User
from authapp.validate import validate_age


class UserCreateForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    age = forms.IntegerField(widget=forms.NumberInput, validators=[validate_age])

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'age',
            'username',
            'email',
            'password1',
            'password2',
        )
