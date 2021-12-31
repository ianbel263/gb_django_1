from django import forms
from django.forms import BaseInlineFormSet

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class OrderInlineFormSet(BaseInlineFormSet):
    pass


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    product_id = forms.CharField(widget=forms.HiddenInput)
    product_name = forms.CharField(label='товар', max_length=50)
    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        fields = ('product_name', 'quantity', 'price')
        exclude = ('product',)

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'product_name':
                field.widget.attrs = {'readonly': True, 'size': '70%'}
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        self.instance = super(OrderItemForm, self).save(commit=False)
        product_pk = self.cleaned_data['product_id']
        self.instance.product = Product.objects.get(pk=product_pk)
        self.instance.save()
        return self.instance
