from django.urls import path

from basketapp.views import add_basket, delete_basket, update_basket

app_name = 'basketapp'
urlpatterns = [
    path('add/<int:product_pk>/', add_basket, name='add_basket'),
    path('delete/<int:pk>/', delete_basket, name='delete_basket'),
    path('update/', update_basket, name='update_basket')
]
