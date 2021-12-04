from django import forms

from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from authapp.validate import validate_age
from mainapp.models import Category


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


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'autofocus': True
    }), label='Наименование категории')
    desc = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control py-4'
    }), required=False, label='Описание категории')

    class Meta:
        model = Category
        fields = ('name', 'desc')
