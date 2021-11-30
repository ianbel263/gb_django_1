from django.urls import path

from basketapp.views import add_basket, delete_basket

app_name = 'basketapp'
urlpatterns = [
    path('add/<int:product_id>', add_basket, name='add_basket'),
    path('delete/<int:basket_id>', delete_basket, name='delete_basket')
]
