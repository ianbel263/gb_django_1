from django import forms

from authapp.forms import UserRegisterForm, UserProfileForm
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


class UserUpdateForm(UserProfileForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False
