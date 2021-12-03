from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authapp.forms import UserRegisterForm
from authapp.models import User


class UserCreateForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    age = forms.IntegerField(widget=forms.NumberInput)

    error_messages = {
        'age_mismatch': _('The age must be at least 18 years old.'),
    }

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

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise ValidationError(
                self.error_messages['age_mismatch'],
                code='age_mismatch'
            )
        return age


