from django import forms

from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from authapp.validate import validate_age
from mainapp.models import Category, Product


def update_widgets(fields):
    labels = {
        'name': 'Наименование',
        'desc': 'Описание',
        'price': 'Цена',
        'image': 'Изображение',
        'quantity': 'Количество',
        'category': 'Категория',
    }

    placeholders = {
        'name': 'Введите наименование',
        'desc': 'Введите описание',
        'price': 'Введите цену',
        'image': 'Загрузите изображение',
        'quantity': 'Введите количество',
        'category': 'Выберите категорию',
    }

    for name, field in fields.items():
        if name == 'image':
            field.widget.attrs['class'] = 'custom-file-input'
        else:
            field.widget.attrs['class'] = 'form-control'
        if name in labels:
            field.label = labels[name]
        if name in placeholders:
            field.widget.attrs['placeholder'] = placeholders[name]


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
    class Meta:
        model = Category
        fields = ('name', 'desc')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        update_widgets(self.fields)
        self.fields['name'].widget.attrs['autofocus'] = True


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'desc', 'image', 'quantity', 'category')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(is_active=True))
        update_widgets(self.fields)
        self.fields['name'].widget.attrs['autofocus'] = True
